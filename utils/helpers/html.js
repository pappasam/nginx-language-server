let compressor = require('html-minifier'),
	compressor_opt = {
		removeComments: true,
		collapseWhitespace: true,
	};

function compress(html = '') {
	return compressor.minify(html, compressor_opt);
}

module.exports = {
	compress
};
