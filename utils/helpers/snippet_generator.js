//@ts-check

let fs = require('fs'),
	chalk = require('chalk'),
	{ ok } = require('./checker');

const bold = any => chalk.bold(String(any));

const SNIPPETS_DIR = `${__dirname}/../../snippets_src/`;

let specialSnippetBody = require('../../snippets_src/_block_with_parameter'),
	extraSnippets = loadExtraSnippets();

let generateBlockSnippetObject = blockName => ({
	prefix: blockName,
	body: specialSnippetBody[blockName] || `${blockName} {\n\t$0\n}`
});
/**
 * @param {Array<any>} directives
 */
function generate(directives) {
	let contextsMap = {},
		result = {};
	directives.forEach(directive =>
		directive.contexts.forEach(context =>
			contextsMap[context] = true));
	//Ignore some contexts
	delete contextsMap.main;
	delete contextsMap.any;

	Object.keys(contextsMap).forEach(blockName =>
		result[`Block ${blockName}`] = generateBlockSnippetObject(blockName));

	Object.keys(extraSnippets).forEach(name => result[name] = extraSnippets[name]);

	return result;
}

function loadExtraSnippets() {
	console.log('Scanning snippet files ...');
	let snippetFileNames = fs.readdirSync(SNIPPETS_DIR)
		.filter(name => !name.startsWith('_') && name.endsWith('.js'));
	let extraSnippets = {};
	ok(); console.log('Total snippet files:', bold(snippetFileNames.length) );
	snippetFileNames.map(fname => require(SNIPPETS_DIR + fname))
		.forEach(snippets =>
			Object.keys(snippets).forEach(name => extraSnippets[name] = snippets[name]));
	console.log('Total snippets:', bold(Object.keys(extraSnippets).length));
	return extraSnippets;
}

module.exports = {
	generate
};
