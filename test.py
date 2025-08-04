import pyvo as vo

service = vo.dal.TAPService("http://dc.g-vo.org/tap")

resultset = service.search("SELECT TOP 1 * FROM ivoa.obscore")
print(resultset)