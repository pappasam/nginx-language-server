//@ts-check

const CACHE_PATH = `${__dirname}/../cache/`;

let request = require('request'),
	chalk = require('chalk'),
	fs = require('fs'),
	checker = require('./checker');

let enable_cache = true;

module.exports = { init, get };

function init(enable_cache) {
	enable_cache || console.log(chalk.yellow.bold(`No cache mode!`));
	if (!fs.existsSync(CACHE_PATH)) {
		console.log(`Creating cache path: ${CACHE_PATH} ...`);
		fs.mkdirSync(CACHE_PATH);
		checker.ok();
	}
}

function get(name, url, callback) {
	process.stdout.write(`HTTP get ${name} `);

	let cacheName = `${CACHE_PATH}${new Buffer(url).toString('base64')}`;
	if (fs.existsSync(cacheName) && enable_cache) {
		console.log(`${chalk.blue('From Cache')}`);
		return callback(fs.readFileSync(cacheName, 'utf8'));
	}

	request.get(url, {}, (err, res, html) => {
		checker.responseOK(name, err, res, html);
		fs.writeFileSync(cacheName, html);

		console.log(`${chalk.green('OK')}`);
		callback(html);
	});
};
