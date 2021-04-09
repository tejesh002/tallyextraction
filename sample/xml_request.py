
GET_COMPANY_LIST = """ 
<ENVELOPE>
    <HEADER>
        <TALLYREQUEST>Export Data</TALLYREQUEST>
    </HEADER>
    <BODY>
        <EXPORTDATA>
            <REQUESTDESC>
                <REPORTNAME> &#4; List of Companies</REPORTNAME>
                <STATICVARIABLES>
                    <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
                </STATICVARIABLES>
            </REQUESTDESC>
        </EXPORTDATA>
    </BODY>
</ENVELOPE>
"""
MASTER_REQUEST = """
<ENVELOPE>
    <HEADER>
        <TALLYREQUEST>Export Data</TALLYREQUEST>
    </HEADER>
    <BODY>
        <EXPORTDATA>
            <REQUESTDESC>
                <REPORTNAME>List of Accounts</REPORTNAME>
                <STATICVARIABLES>
                    <SVCURRENTCOMPANY>{}</SVCURRENTCOMPANY>
                    <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
                    <ACCOUNTTYPE>All Masters</ACCOUNTTYPE>
                </STATICVARIABLES>
            </REQUESTDESC>
        </EXPORTDATA>
    </BODY>
</ENVELOPE>
"""

VOUCHER_REQUEST = """
<ENVELOPE>
    <HEADER>
        <TALLYREQUEST>Export Data</TALLYREQUEST>
    </HEADER>
    <BODY>
        <EXPORTDATA>
            <REQUESTDESC>
                <STATICVARIABLES>
                    <SVCURRENTCOMPANY>{}</SVCURRENTCOMPANY>
                    <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
                    <SVFROMDATE>{}</SVFROMDATE>
                    <SVTODATE>{}</SVTODATE>
                    <RTSSVLEDGERNAME>ALL MASTERS</RTSSVLEDGERNAME>
                </STATICVARIABLES>
                <REPORTNAME>Voucher Register</REPORTNAME>
            </REQUESTDESC>
        </EXPORTDATA>
    </BODY>
</ENVELOPE>
"""

GET_COMPANY_LIST_PRIME = """
<ENVELOPE>
	<HEADER>
		<VERSION>
			1
		</VERSION>
		<TALLYREQUEST>
			Export
		</TALLYREQUEST>
		<TYPE>
			Data
		</TYPE>
		<ID>
			List of Companies
		</ID>
	</HEADER>
	<BODY>
		<DESC>
			<TDL>
				<TDLMESSAGE>
					<REPORT NAME="List of Companies" ISMODIFY="No" ISFIXED="No" ISINITIALIZE="No" ISOPTION="No" ISINTERNAL="No">
						<FORMS>
							List of Companies
						</FORMS>
					</REPORT>
					<FORM NAME="List of Companies" ISMODIFY="No" ISFIXED="No" ISINITIALIZE="No" ISOPTION="No" ISINTERNAL="No">
						<TOPPARTS>
							List of Companies
						</TOPPARTS>
						<XMLTAG>
							"List of Companies"
						</XMLTAG>
					</FORM>
					<PART NAME="List of Companies" ISMODIFY="No" ISFIXED="No" ISINITIALIZE="No" ISOPTION="No" ISINTERNAL="No">
						<TOPLINES>
							List of Companies
						</TOPLINES>
						<REPEAT>
							List of Companies : Collection of Companies
						</REPEAT>
						<SCROLLED>
							Vertical
						</SCROLLED>
					</PART>
					<LINE NAME="List of Companies" ISMODIFY="No" ISFIXED="No" ISINITIALIZE="No" ISOPTION="No" ISINTERNAL="No">
						<LEFTFIELDS>
							Name
						</LEFTFIELDS>
					</LINE>
					<FIELD NAME="Name" ISMODIFY="No" ISFIXED="No" ISINITIALIZE="No" ISOPTION="No" ISINTERNAL="No">
						<SET>
							$Name
						</SET>
						<XMLTAG>
							"NAME"
						</XMLTAG>
					</FIELD>
					<COLLECTION NAME="Collection of Companies" ISMODIFY="No" ISFIXED="No" ISINITIALIZE="No" ISOPTION="No" ISINTERNAL="No">
						<TYPE>
							Company
						</TYPE>
					</COLLECTION>
				</TDLMESSAGE>
			</TDL>
		</DESC>
	</BODY>
</ENVELOPE>
"""