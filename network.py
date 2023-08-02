import geoip2.database
reader = geoip2.database.Reader('GeoLite2-Country.mmdb')
response = reader.country('192.168.105.242')
print(response.country.name)