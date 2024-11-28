class TableBuilder:
    table = """<html>
<body>
    <table border="1" cellpadding="5" cellspacing="0">
        <tr>
            <th>IP</th>
            <th>Service Name</th>
            <th>Status</th>
        </tr>"""
    def __init__(self):
        pass

    def addRow(self,ip_address,service_name,status):
        row = f"""        <tr>
            <td>{ip_address}</td>
            <td>{service_name}</td>
            <td>{status}</td>
        </tr>"""

        self.table += row 

        return self 
    
    def build(self):
        ending = """</table></body></html>"""
        self.table += ending 
        return self.table
    





def check():
    tb = TableBuilder()
    tb.addRow("13.12.12.11","Chronyd","Active:(active)running")
    tb.addRow("13.12.12.11","Chronyd","Active:(active)running")
    tb.addRow("13.12.12.11","Chronyd","Active:(active)running")
    table = tb.build()
    print(table)

#check()