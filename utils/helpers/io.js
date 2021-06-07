//@ts-check

let fs = require('fs');

module.exports = { writeEachJSON, writeJSON };

/**
 * @param {{[fileName: string]: any}} jsonMap
 */
function writeEachJSON(jsonMap) {
	return Promise.all(
		Object.keys(jsonMap).map(filePath => writeJSON(filePath, jsonMap[filePath])));
}

/**
 * @param {string} filePath
 */
function writeJSON(filePath, object) {
	return new Promise((resolve, reject) => {
		fs.writeFile(filePath, JSON.stringify(object, null, 2) + '\n', err =>
			err ? reject(err) : resolve());
	});
}
