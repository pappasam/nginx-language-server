#!/usr/bin/env node
//@ts-check

const ENABLE_CACHE = process.argv[2] != '--no-cache';

const BASE_URL = 'https://nginx.org/en/docs/';
const SIGN_TITLE = 'Modules reference';
const SIGN_TABLE_HEAD = 'Syntax:Default:Context:';
const SIGN_SINCE_VERSION = /^This directive appeared in versions? (\d+\.\d+\.\d+)/;

const OUTPUT = `${__dirname}/../nginx_language_server/data`;

const DIRECTIVES_OUTPUT_FILE = `${OUTPUT}/directives.json`;
const VARIABLES_OUTPUT_FILE = `${OUTPUT}/variables.json`;
const SNIPPETS_OUTPUT_FILE = `${OUTPUT}/snippets.json`;
const DIRECTIVES_DOC_OUTPUT_FILE = `${OUTPUT}/directives_document.json`;
const VARIABLES_DOC_OUTPUT_FILE = `${OUTPUT}/variables_document.json`;

const chalk = require('chalk');
const url = require('url');
const cheerio = require('cheerio');

const checker = require('./lib/checker');
const snippetGenerator = require('./lib/snippet_generator');
const http = require('./lib/http_with_cache');
const html = require('./lib/html');
const io = require('./lib/io');

const bold = any => chalk.bold(String(any));
const removeBlank = any => String(any).replace(/\s/g, '');

let start = name => console.log(`${name} ...`);

const newVariableObject = () => ({
	name: '',
	desc: '',
	module: ''
});
const newDirectiveObject = () => ({
	name: '',
	syntax: [],
	def: '',
	contexts: [],
	desc: '',
	notes: [],
	since: '',
	module: ''
});
const newDirectiveDocObject = () => ({
	table: '',
	doc: '',
	module: '',
	link: '',
	name: ''
});
const newVariableDocObject = () => ({
	module: '',
	vars: {},
	doc: ''
});


//==========================
//     START      =======>
let pageList = [];
let directivesResult = [];
let variablesResult = [];
let directivesDocResult = [];
let variablesDocResult = [];
let snippetsResult = {};
let lastDirectivesLength = 0;
let lastVariablesLength = 0;

main();

function main() {
	http.init(ENABLE_CACHE);
	http.get('Nginx document index page', BASE_URL, html => {
		checker.ok();

		start('Analyzing sub document page links');
		let $ = cheerio.load(html),
			title = $('center h4').filter((i, e) => $(e).text().trim() == SIGN_TITLE);
		checker.lengthEquals('document page title "Modules reference"', title, 1);

		let directiveLists = title.parent().nextAll('ul.compact');
		checker.lengthEquals('ul.compact', directiveLists, 6, checker.LEVEL_WARN);

		directiveLists.each((i, list) => {
			//ignore
			//  Alphabetical index of directives
			//  Alphabetical index of variables
			if (i == 0) return;
			let links = $(list).find('a'), link;
			checker.lengthAtLease('<a> in ul.compact', links, 1);
			links.each(i => {
				link = links.eq(i);
				pageList.push({ uri: link.attr('href'), name: link.text().trim() });
			});
		});
		checker.ok(`Got ${bold(pageList.length)} sub document pages`);

		handlerSubDocumentPage();
	});
}

function finish() {
	start('Generating snippet object array');
	snippetsResult = snippetGenerator.generate(directivesResult);
	checker.ok();

	start('Writing to file');
	io.writeEachJSON({
		[DIRECTIVES_OUTPUT_FILE]: directivesResult,
		[DIRECTIVES_DOC_OUTPUT_FILE]: directivesDocResult,
		[VARIABLES_OUTPUT_FILE]: variablesResult,
		[VARIABLES_DOC_OUTPUT_FILE]: variablesDocResult,
		[SNIPPETS_OUTPUT_FILE]: snippetsResult,
	});
	checker.ok();

	console.log(`Total directives number: ${bold(directivesResult.length)}`);
	console.log(`Total variables number: ${bold(variablesResult.length)}`);

	return checker.done();
}

function handlerSubDocumentPage() {
	if (pageList.length === 0)
		return finish();

	let { uri, name } = pageList.shift();
	let fullURL = `${BASE_URL}${uri}`;

	http.get(`sub-page ${bold(name)}`, fullURL, _html => {
		checker.ok();
		let $ = cheerio.load(_html),
			directives = $('.directive'),
			variableContainer = $('a[name=variables]')

		start(`Analyzing sub-page ${bold(name)}`);

		checker.lengthAtLease(`directives info of ${name}: .directive`, directives, 1);

		directives.each(i => {
			let item = newDirectiveObject(),
				docObj = newDirectiveDocObject();

			let directive = directives.eq(i);

			docObj.table = html.compress(directive.html())
				.replace('cellspacing=\"0\"', '');

			//check table item available
			let title_check = removeBlank(directive.find('table th').text());
			checker.equal('directive define table head', title_check, SIGN_TABLE_HEAD);

			let directiveDef = directive.find('table td');
			checker.lengthEquals('directive define item', directiveDef, 3);

			let directiveSyntax = directiveDef.eq(0),
				directiveDefault = directiveDef.eq(1),
				directiveContext = directiveDef.eq(2);

			item.module = name;
			docObj.module = name;

			item.name = directiveSyntax.find('code strong').eq(0).text().trim();
			docObj.name = item.name;
			checker.lengthAtLease(`directive name in module(${name})`, item.name, 1);

			directiveSyntax.children('code').each((i, e) => item.syntax.push($(e).text().trim()));
			checker.lengthAtLease(`directive syntax (${item.name})`, item.syntax, 1);
			item.syntax.forEach((syntax, i) =>
				checker.lengthAtLease(`directive syntax[${i}] (${item.name})`, syntax, item.name.length));

			item.def = directiveDefault.text().trim();
			item.def = item.def == '—' ? null : item.def;

			item.contexts = removeBlank(directiveContext.text()).split(',');
			checker.lengthAtLease(`directive contexts (${item.name})`, item.contexts, 1);

			item.since = directive.find('p').text().trim() || null;
			if (item.since) {
				item.since = (item.since.match(SIGN_SINCE_VERSION) || ['', null])[1];
				checker.lengthAtLease(`directive since version (${item.name})`, item.since, 1);
			}

			docObj.link = directive.prev('a').attr('name');
			checker.lengthAtLease(`document link of directive (${item.name})`, docObj.link, 1);
			docObj.link = `${uri}#${docObj.link}`;

			// loop after directive box div

			let elementPointer = directive;
			while ((elementPointer =
				elementPointer.next('p, blockquote.note, blockquote.example, dl.compact')).length) {
				let tagName = elementPointer.prop('tagName');
				switch (tagName) {
					case 'P':
						if (!elementPointer.text().trim()) continue;
						if (!item.desc)
							item.desc = elementPointer.text().replace(/\n/g, ' ').replace(/\s{2,}/g, ' ').trim();
						docObj.doc += $.html(elementPointer);
						break;
					case 'DL':
						docObj.doc += $.html(elementPointer);
						break;
					case 'BLOCKQUOTE':
						let className = elementPointer.attr('class').trim();
						if (className == 'note')
							item.notes.push(elementPointer.text());
						else if (className != 'example')
							checker.warn(`there is a blockquote tag with unknown class name (${className}) ` +
								`after directive (${item.name})`);
						docObj.doc += $.html(elementPointer);
				}
			}

			checker.lengthAtLease(`description of directive (${item.name})`, item.desc, 1, checker.LEVEL_WARN);
			// checker.lengthAtLease(`document content of directive (${item.name})`, item.doc, 1);

			docObj.doc = resolveDocumentHTML(docObj.doc);

			directivesResult.push(item);
			directivesDocResult.push(docObj);
		});

		if (variableContainer.length) {
			let docObj = newVariableDocObject();
			docObj.module = name;

			let variablesDescription = variableContainer.next('center').next('p');
			let container = variablesDescription.next('dl');

			//Because page of ngx_http_auth_jwt_module
			if (!container.length)
				container = variablesDescription.next('p').next('dl');

			checker.lengthEquals(`variables info of ${name}: a[name=variables]+center+p+dl or ` +
				`a[name=variables]+center+p+p+dl`,
				container, 1);

			docObj.doc = $.html(variablesDescription);
			if (variablesDescription.next('p').length)
				docObj.doc += $.html(variablesDescription.next('p')) + $.html(container);
			else
				docObj.doc += $.html(container);
			docObj.doc = resolveDocumentHTML(docObj.doc);

			// too many page has not compact class in variable
			// if ((container.attr('class')||'').trim() != 'compact')
			// 	checker.warn(`variables dl tag has not class name "compact" in ${name}`);

			container.children('dt').each((i, e) => {
				let elementVarName = $(e),
					elementVarDesc = elementVarName.next('dd'),
					elementTailCheck = elementVarName.next().next(),
					item = newVariableObject();

				item.module = name;
				item.name = (elementVarName.text() || '').trim();
				checker.lengthAtLease(`variable name ${i} of ${name}`, item.name, 2);

				item.desc = (elementVarDesc.text() || '').trim();
				checker.lengthAtLease(`description of variable ${item.name}`, item.desc, 1);

				if (elementTailCheck.length && elementTailCheck.prop('tagName') != 'DT')
					checker.warn(`the tag after description of variable ${item.name} is not "dt"`);

				let elementId = elementVarName.attr('id');
				checker.lengthAtLease(`attribute "id" of element "dt" ${item.name} `,
					elementId, 'var_'.length);

				docObj.vars[item.name] = elementId;
				variablesResult.push(item);
			});

			variablesDocResult.push(docObj);
		}


		let diffDirectives = directivesResult.length - lastDirectivesLength,
			diffVariables = variablesResult.length - lastVariablesLength;

		diffDirectives && console.log(` - Directives count: ${bold(diffDirectives)}`);
		diffVariables && console.log(` - Variables count: ${bold(diffVariables)}`);

		lastDirectivesLength += diffDirectives;
		lastVariablesLength += diffVariables;

		checker.ok();

		handlerSubDocumentPage();
	});

	function resolveDocumentHTML(docHTML) {
		return html.compress(docHTML).replace(/href=[\"\'](.+?)[\"\']/g,
			(_, href) => `href="${encodeURI(url.resolve(fullURL, decodeURI(href)))}"`);
	}
}
