#!/usr/bin/python

def run(val):
	ret = []
	ret += spamhouse(val)
	ret += sorbs(val)
	return ret

def sorbs(val):
	from dns import resolver
	s_codes = {
		'127.0.0.2':	'http.dnsbl.sorbs.net\nList of Open HTTP Proxy Servers',
		'127.0.0.3':	'socks.dnsbl.sorbs.net\nList of Open SOCKS Proxy Servers',
		'127.0.0.4':	'misc.dnsbl.sorbs.net\nList of open Proxy Servers not listed in the SOCKS or HTTP lists',
		'127.0.0.5':	'smtp.dnsbl.sorbs.netn\nList of Open SMTP relay servers',
#		'127.0.0.6':	'new.spam.dnsbl.sorbs.net\nList of hosts that have been noted as sending spam/UCE/UBE to the admins of SORBS within the last 48 hours.',
#		'127.0.0.6':	'recent.spam.dnsbl.sorbs.net\n',
#		'127.0.0.6':	'old.spam.dnsbl.sorbs.net\n',
		'127.0.0.6':	'spam.dnsbl.sorbs.net\nList of hosts that have been noted as sending spam/UCE/UBE to the admins of SORBS',
#		'127.0.0.6':	'escalations.dnsbl.sorbs.net\n',
		'127.0.0.7':	'web.dnsbl.sorbs.net\nList of web (WWW) servers which have spammer abusable vulnerabilities (e.g. FormMail scripts)\nNote: This zone now includes non-webserver IP addresses that have abusable vulnerabilities',
		'127.0.0.8':	'block.dnsbl.sorbs.net\nList of hosts demanding that they never be tested by SORBS',
		'127.0.0.9':	'zombie.dnsbl.sorbs.net\nList of networks hijacked from their original owners, some of which have already used for spamming',
		'127.0.0.10':	'dul.dnsbl.sorbs.net\nDynamic IP Address ranges',
		'127.0.0.11':	'badconf.rhsbl.sorbs.net\nList of domain names where the A or MX records point to bad address space',
		'127.0.0.12':	'nomail.rhsbl.sorbs.net\nList of domain names where the owners have indicated no email should ever originate from these domains',
		'127.0.0.14':	'noserver.dnsbl.sorbs.net\nIP addresses and Netblocks of where system administrators and ISPs owning the network have indicated that servers should not be present',
		'127.0.0.15':	'virus.dnsbl.sorbs.net\nHosts that have delivered known viruses to the SORBS spamtrap servers in the last 7 days'
	}
	ret = []
	src = {'method': 'chk_blacklist', 'type': 'ip', 'value': val}
	revip = ".".join(val.split('.')[::-1])

	sh_ret = []
	sh_val = revip + '.dnsbl.sorbs.net'
	spamhouse = {
		'method': 'check blacklists',
		'type': 'text',
		'value': 'sorbs'
	}
	ret.append({'request': src, 'response': spamhouse})
	try:
		sh_query = resolver.query(sh_val, "A")
	except:
		sh_ret.append('spamhouse: ok')
	else:
		for r in sh_query:
			ret.append({'request': spamhouse, 'response': {
				'method': 'query spamhouse',
				'type': 'text',
				'value': s_codes[str(r)]
			}})
	return ret



def spamhouse(val):
	from dns import resolver
	sh_codes = {
		'127.0.1.2':	'spam domain',
		'127.0.1.4':	'phish domain',
		'127.0.1.5':	'malware domain',
		'127.0.1.6':	'botnet C&C domain',
		'127.0.1.102':	'abused legit spam',
		'127.0.1.103':	'abused spammed redirector domain',
		'127.0.1.104':	'abused legit phish',
		'127.0.1.105':	'abused legit malware',
		'127.0.1.106':	'abused legit botnet C&C',
		'127.0.1.255':	'IP queries prohibited!',
		#Return Code 	Zone 	Description
		'127.0.0.2':	'SBL: Spamhaus SBL Data, Static UBE sources, verified spam services (hosting or support) and ROKSO spammers',
		'127.0.0.3':	'SBL: Spamhaus SBL CSS Data, Static UBE sources, verified spam services (hosting or support) and ROKSO spammers',
		'127.0.0.9':	'SBL: Spamhaus DROP/EDROP Data, Static UBE sources, verified spam services (hosting or support) and ROKSO spammers',
		'127.0.0.4':	'XBL: CBL Data, Illegal 3rd party exploits, including proxies, worms and trojan exploits',
		'127.0.0.5':	'XBL: CBL Data, Illegal 3rd party exploits, including proxies, worms and trojan exploits',
		'127.0.0.6':	'XBL: CBL Data, Illegal 3rd party exploits, including proxies, worms and trojan exploits',
		'127.0.0.7':	'XBL: CBL Data, Illegal 3rd party exploits, including proxies, worms and trojan exploits',
		'127.0.0.10':	'PBL: ISP Maintained, IP ranges which should not be delivering unauthenticated SMTP email.',
		'127.0.0.11':	'PBL: Spamhaus Maintained, IP ranges which should not be delivering unauthenticated SMTP email.'
	}
	ret = []
	src = {'method': 'chk_blacklist', 'type': 'ip', 'value': val}
	revip = ".".join(val.split('.')[::-1])

	sh_ret = []
	sh_val = revip + '.zen.spamhaus.org'
	spamhouse = {
		'method': 'check blacklists',
		'type': 'text',
		'value': 'spamhouse'
	}
	ret.append({'request': src, 'response': spamhouse})
	try:
		sh_query = resolver.query(sh_val, "A")
	except:
		sh_ret.append('spamhouse: ok')
	else:
		for r in sh_query:
			seg = str(r).split('.')
			if seg[2] == '0':	v='Spamhaus IP Blocklist\n' + sh_codes[str(r)]
			if seg[2] == '1':	v='Spamhaus Domain Blocklist\n' + sh_codes[str(r)]
			if seg[2] == '2':	v='Spamhaus whitelist'
			ret.append({'request': spamhouse, 'response': {
				'method': 'query spamhouse',
				'type': 'text',
				'value': v
			}})
	return ret
