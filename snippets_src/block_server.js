module.exports = {
	"Block server with directives": {
		prefix: 'server',
		body: [
			'server {',
			'\tlisten ${address:80};',
			'\tserver_name ${server_names};',
			'\taccess_log  ${logs/server.access.log} main;',
			'\t$0',
			'}'
		]
	}
};