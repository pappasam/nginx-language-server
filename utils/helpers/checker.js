let chalk = require('chalk');

const bold = any => chalk.bold(String(any));

const OK = ' - ' + chalk.green('OK');
const WARN = ' - ' + chalk.yellow('WARN');
const ERROR = ' - ' + chalk.red('ERROR');
const DONE = chalk.blue.bold('DONE');
const LEVEL_WARN = true;
const LEVEL_ERROR = false;

/**
 * @param {String} reason
 */
function error(reason = '') {
	console.error(ERROR, '\n', reason);
	process.exit(1);
}
function warn(reason = '') {
	console.warn(WARN, '\n', reason);
}
function ok(what = '') {
	console.log(OK, what);
}
function done() {
	console.log(DONE);
}

/**
 * @param {string} name
 * @param {{length: number}} arrOrStr
 * @param {number} length
 * @param {boolean} justWarn
 */
function lengthEquals(name = '', arrOrStr = [], length = 1, justWarn = false) {
	return (arrOrStr && arrOrStr.length == length) ?
		arrOrStr :
		(justWarn ? warn : error)(`length of ${bold(name)} (${
			arrOrStr ? arrOrStr.length : 'undefined'})is not equal ${bold(length)}!`);
}
/**
 *
 * @param {string} name
 * @param {{length: number}} arrOrStr
 * @param {number} length
 * @param {boolean} justWarn
 */
function lengthAtLease(name, arrOrStr, length = 1, justWarn = false) {
	return (arrOrStr && arrOrStr.length >= length) ?
		arrOrStr :
		(justWarn ? warn : error)(`length of ${bold(name)} (${
			arrOrStr ? arrOrStr.length : 'undefined'})less than ${bold(length)}!`);
}
function responseOK(name, err, res, html) {
	err && error(err.stack);
	res.statusCode != 200 && error(`${bold(name)} statusCode != 200`);
	!html && error(`${bold(name)} empty response content`);
}
function equal(name = '', actual = '', expected = '', justWarn = false) {
	if (actual === expected)
		return true;
	(justWarn ? warn : error)(`${bold(name)}: expected: ${chalk.green(expected)}` +
		`.But actual: ${chalk.red(actual)}.`);
}

module.exports = {
	ok, error, warn, done, LEVEL_ERROR, LEVEL_WARN,
	lengthEquals,
	lengthAtLease,
	responseOK,
	equal
};
