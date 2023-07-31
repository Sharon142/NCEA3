import geoip2.database
reader = geoip2.database.Reader('GeoLite2-Country.mmdb')
response = reader.country('128.101.101.101')
print(response.country.name)