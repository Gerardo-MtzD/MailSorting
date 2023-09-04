from random import uniform


class get_xml:
    """Gets relevant information from xml and processess it"""

    def __init__(self, file_path: str, xml, csv: dict, list_to_trash: list, month: str, year: int):
        # CALLS ALL FUNCTIONS TO RETRIEVE RELEVANT INFO
        self.filePath = file_path
        self.csv = csv
        self.list_to_trash = list_to_trash
        self.new_dict = xml
        self.month = 0
        self.year = 0
        self.impuesto = 0.0
        self.name = str()
        self.subtotal = 0.0
        self.total = 0.0
        if '.xml' in str(self.filePath)[-4:]:
            self.get_info_str()
        self.update_csv(month, year)

    def handle_item(_, item):
        print(item)

    def get_info(self) -> None:
        self.concept = self.new_dict['cfdi:Comprobante']['cfdi:Emisor']['@Nombre']
        self.name = self.new_dict['cfdi:Comprobante']['cfdi:Receptor']['@Rfc']
        try:
            self.folio = self.new_dict['cfdi:Comprobante']['@Folio']
        except KeyError:
            self.folio = f'{int(uniform(1, 1000))}'
            # print("Folio not found")
        # GET AMOUNTS
        self.subtotal = float(self.new_dict['cfdi:Comprobante']['@SubTotal'])
        try:
            self.impuesto = float(self.new_dict['cfdi:Comprobante']['cfdi:Impuestos']['@TotalImpuestosTrasladados'])
        except (KeyError, TypeError):
            self.impuesto = float(0.0)
        self.total = float(self.new_dict['cfdi:Comprobante']['@Total'])
        # FINDING DATE OF CREATION
        self.date = self.new_dict['cfdi:Comprobante']['@Fecha']
        self.year = self.date[0:4]
        self.month = self.date[5:7]

    def get_info_backup(self) -> None:
        for root in self.new_dict.iter():
            for child in root:
                tab = child.tag.split('}')[-1]
                if tab == 'Emisor':
                    self.concept = child.attrib['Nombre']
                elif tab == 'Receptor':
                    self.name = child.attrib['Rfc']
                elif tab == 'Traslado':
                    try:
                        if child.attrib['Base']:
                            self.subtotal = float(child.attrib['Base'])
                            try:
                                self.impuesto = float(child.attrib['Importe'])
                            except:
                                self.impuesto = 0.0
                            self.total = self.subtotal + self.impuesto
                    except KeyError:
                        pass
        self.folio = f'r{int(uniform(1, 10000))}'
        self.year = 0
        self.month = 0

    def get_info_str(self) -> None:
        self.folio = f'str{int(uniform(1, 10000))}'
        my_xml = self.new_dict.split('>')
        for i, row in enumerate(my_xml):
            element = row.split(' ')
            if "Receptor" in row and len(element) > 1:
                for c in element:
                    if "Rfc" in c:
                        subject, name = c.split('="')
                        self.name = name[:-1]
                        #print(f"name: {self.name}")
            if "Emisor" in row and len(element) > 1:
                for c in row.split('" '):
                    if "Nombre" in c:
                        subject, concept = c.split('="')
                        self.concept = concept
                        #print(f"concept: {self.concept}")
            if 'Folio' in row:
                for c in row.split('" '):
                    if "Folio" in c:
                        _, folio = c.split('="')
                        self.folio = folio
                        #print(f"folio: {self.folio}")
            for c in element:
                if "Total" in c:
                    try:
                        subject, amount = c.split('="')
                    except ValueError:
                        print(f"E: IN -> {self.filePath}")
                        break
                    if len(subject) == 5:
                        self.total = float(amount[:-1])
                        #print(self.total)
                    elif len(subject) == 8:
                        self.subtotal = float(amount[:-1])
                        #print(self.subtotal)
                    elif 'TotalImpuestosTrasladados' in subject:
                        subject, amount = c.rstrip().split('="')
                        self.impuesto = float(amount[:-1])
                        #print(self.impuesto)
                if "Fecha" in c:
                    try:
                        subject, date = c.split('="')
                        date = date.split("T")[0]
                        self.year = date[0:4]
                        self.month = date[5:7]
                    except ValueError:
                        print("ERROR IN DATE")
                        print(c)
                    #print(self.year, self.month)


    def update_csv(self, month_search: str, year_search: int) -> None:
        if int(self.month) == int(month_search[:2]) and int(self.year) == int(year_search) or (
                self.month == 0 or self.year == 0):
            if self.name == 'TSE090522B18' or self.name == 'MAMG650207659' or self.name == 'DEMR650805NP2':
                self.csv.update({self: [self.name, self.folio, self.concept, self.subtotal, self.impuesto, self.total,
                                        self.filePath]})
            else:
                print(f"NO MATCH FOUND for Document {self.filePath}")
                # send2trash(self.filePath)
                # self.csv.update({self: [self.name, self.concept, self.subtotal, self.impuesto, self.total]})
                self.list_to_trash.append(self.filePath)
        else:
            print(f"Document {self.filePath} does not belong to correct date")
            self.list_to_trash.append(self.filePath)
