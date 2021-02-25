/**
 * In default, each snippet of block in nginx.conf likes followed:
 *
 * "Block blockName": {
 *   "prefix": "blockName",
 *   "body": "blockName {\n\t$0\n}"
 * },
 *
 * But there are some special blocks with parameters, likes: location, upstream
 * So define these special blocks in here: 
 */

module.exports = {
	location: 'location ${location:/} {\n\t$0\n}',
	upstream: 'upstream ${upstream_name} {\n\t$0\n}'
};