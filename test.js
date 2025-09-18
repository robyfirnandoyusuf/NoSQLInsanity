// const couchbase = require('couchbase');
import * as couchbase from 'couchbase';


async function runQuery() {
    const cluster = await couchbase.connect('couchbase://localhost', {
        username: 'Administrator',
        password: 'root123',
    });

    // const bucket = cluster.bucket('travel-sample');
    // const scope = bucket.scope('_default');

    try {
      
        const bucket = cluster.bucket('travel-sample');
        const scope = bucket.scope('inventory');
        // const rows2 = await scope.query('SELECT a.* FROM `airline` AS a LIMIT 5;');
        const rows2 = await scope.query(
            'SELECT h.* FROM `hotel` AS h LIMIT 5;'
        );
        console.log('Couchbase Buckets:');
        console.log('Query Results:', rows2);
    } catch (error) {
        console.error('Query failed:', error);
    } finally {
        await cluster.close();
    }
}

runQuery();