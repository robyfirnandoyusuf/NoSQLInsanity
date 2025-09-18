import express from 'express';
import 'dotenv/config';
import * as couchbase from 'couchbase';
import helmet from 'helmet';
// import rateLimit from 'express-rate-limit';
// import morgan from 'morgan';
import bodyParser from 'body-parser';

// ---- infra / security-ish middlewares ----
const app = express();
app.use(helmet());
app.use(bodyParser.json());
// app.use(morgan('combined'));
// app.use(rateLimit({
//   windowMs: 60_000, // 1 menit
//   max: 120,         // 120 req/menit per IP
// }));
console.log(process.env.COUCHBASE_USERNAME)
// ---- couchbase connect ----
// const cluster = await couchbase.connect(`couchbase://${process.env.COUCHBASE_HOST}`, {
//   username: process.env.COUCHBASE_USERNAME,
//   password: process.env.COUCHBASE_PASSWORD,
// });
// const bucket = cluster.bucket(process.env.COUCHBASE_BUCKET);
// const scope = bucket.scope('_default'); // pakai default scope

var cluster = new couchbase.Cluster('couchbase://' + process.env.COUCHBASE_HOST);
// myCluster.authenticate(process.env.COUCHBASE_ADMIN_USER, process.env.COUCHBASE_ADMIN_PASSWORD);
var cluster = await couchbase.connect('couchbase://localhost', {
    username: 'Administrator',
    password: 'root123',
})
console.log(process.env.COUCHBASE_BUCKET)
var bucket = cluster.bucket(process.env.COUCHBASE_BUCKET);
// NOTE: kita pakai cluster.query() untuk N1QL

// Helper: wrap query dengan timeout & named params
async function q(sql, params = {}, options = {}) {
  const res = await cluster.query(sql, {
    parameters: params,
    timeout: options.timeout || 5_000, // 5s
    readonly: true,
  });
  return res.rows;
}

// Helper: validasi input sederhana biar “realistic”
function requireString(name, val, {max = 64, allowEmpty = false} = {}) {
  if (typeof val !== 'string') throw new Error(`${name} harus string`);
  const trimmed = val.trim();
  if (!allowEmpty && trimmed.length === 0) throw new Error(`${name} kosong`);
  if (trimmed.length > max) throw new Error(`${name} terlalu panjang`);
  return trimmed;
}

// ---- Routes ----
app.get('/', (req, res) => {
  res.send('OK. Try: GET /breweries?city=Los%20Angeles  or  GET /hotels/search?city=San%20Francisco&q=Inn');
});

/**
 * GET /breweries?city=Los%20Angeles
 * Contoh realistis: daftar brewery di suatu kota.
 * Aman karena pakai named parameters ($city).
 */
app.get('/breweries', async (req, res) => {
  try {
    const city = requireString('city', req.query.city || '');
    console.log(city)
    const sql = `
      SELECT name, address, city, state, phone
      FROM \`${process.env.COUCHBASE_BUCKET}\`
      ORDER BY name
      LIMIT 50
    `;
    const rows = await q(sql, { city });
    res.json({ ok: true, count: rows.length, rows });
  } catch (e) {
    res.status(400).json({ ok: false, error: e.message });
  }
});

/**
 * GET /hotels/search?city=San%20Francisco&q=Inn
 * Pencarian “name LIKE %q%” yang aman dengan parameterisasi.
 * Perhatikan kita membangun wildcard di JS, bukan menyelipkan string mentah di SQL.
 * query blind: http://localhost:3000/hotels/search?city=San Francisco' AND '{' = SUBSTR(ENCODE_JSON((SELECT * FROM system:keyspaces ORDER BY id)), 1, 1) -- -&q=Inn
 */
app.get('/hotels/search', async (req, res) => {
  try {
    console.log('asd')
    const city = req.query.city;
    const qtext = req.query.q;

    // const query = `
    //   SELECT h.name, h.city, h.state, h.address, h.phone
    //   FROM \`${process.env.COUCHBASE_BUCKET}\` AS h
    //   WHERE h.type = "hotel"
    //     AND h.city = ${city}
        
    //   ORDER BY h.name
    //   LIMIT 50;
    // `;

    // /* const options = {
    //   parameters: {
    //     city,
    //     pattern: `%${qtext}%`
    //   }
    // }; */

    // const res = await cluster.query(query);
    // console.log(res.rows)
    const bucketx = cluster.bucket('travel-sample');
    const scope = bucketx.scope('inventory');
    // console.log(scopex)
    // const result = await scope.query('SELECT h.name, h.city, h.state, h.address, h.phone FROM `travel-sample` WHERE type = "airline" LIMIT 10');
    const rows = await scope.query(
            `SELECT h.* FROM \`hotel\` as h WHERE h.city = '${city}' LIMIT 5;`
      );
    console.log('Query Results:', rows);
    res.json({ ok: true, count: rows.length, rows });
  } catch (e) {
    res.status(400).json({ ok: false, error: e.message });
  }
});

/**
 * POST /auth/login
 * Body: { "username": "...", "password": "..." }
 * Contoh "auth" yang terlihat realistis: kita lookup user doc di bucket lain/sama.
 * Di lab ini, kita cuma return “fake” decision supaya tetap self-contained.
 * (Gunakan parameterisasi untuk menghindari injection saat lookup berdasarkan username.)
 */
app.post('/auth/login', async (req, res) => {
  try {
    const username = requireString('username', req.body?.username || '');
    // WARNING: Di real app, password harus di-hash & diverifikasi pakai bcrypt.
    // Di lab ini kita gak query password ke N1QL untuk menghindari pola rentan.

    const sql = `
      SELECT META(u).id AS id, u.username, u.role
      FROM \`${process.env.COUCHBASE_BUCKET}\` AS u
      WHERE u.type = "user" AND u.username = $username
      LIMIT 1
    `;
    const [user] = await q(sql, { username });

    if (!user) {
      return res.status(401).json({ ok: false, error: 'Invalid credentials' });
    }
    // Anggap password match (lab). Di real-world, bandingkan hash!
    res.json({ ok: true, user: { id: user.id, username: user.username, role: user.role } });
  } catch (e) {
    res.status(400).json({ ok: false, error: e.message });
  }
});

// ---- start ----
const port = process.env.APPLICATION_PORT || 3000;
app.listen(port, () => {
  console.log(`Listening on http://localhost:${port}`);
});
