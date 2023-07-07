
from project_willy.settings import RecordReprSettings, RecordsBookReprSettings
from project_willy.text_fields import MethodsText

class RecordRepr(RecordReprSettings):

    def show_record(self) -> str:
        result = ''

        # name as title
        if self.name:
            result += self.general_title.format(self.name.get_str(), self.line_of_general_row)
        else:
            result += self.general_title.format(f'Name: {MethodsText.DEFAULT_EMPTY_FIELD}', self.line_of_general_row)

        # phones
        if self.phones:
            result += self.general_row_pattern.format(self.phones[0].get_str(), self.line_of_general_row)
            if len(self.phones) > 1:
                for phone in self.phones[1:]:
                    result += self.general_row_pattern.format(phone.get_str(), self.line_of_general_row)            
        else:
            result += self.general_row_pattern.format(f'Phone: {MethodsText.DEFAULT_EMPTY_FIELD}', self.line_of_general_row)        

        # email
        if self.email:
            result += self.general_row_pattern.format(f'Email: {self.email.get_str()}', self.line_of_general_row)
        else:
            result += self.general_row_pattern.format(f'Email: {MethodsText.DEFAULT_EMPTY_FIELD}', self.line_of_general_row)

        # birthday
        if self.birthday:
            result += self.general_row_pattern.format(f'Birthday: {self.birthday.get_str()}', self.line_of_general_row)
        else:
            result += self.general_row_pattern.format(f'Birthday: {MethodsText.DEFAULT_EMPTY_FIELD}', self.line_of_general_row)       

        return result  


class RecordsBookRepr(RecordsBookReprSettings):

    def table_head(self) -> str:
        result = self.table_title.format('---RECORDS BOOK---', self.line_of_table_row)
        result += self.table_row_pattern.format('No', 'Name', 'Phone', 'Email', 'Birthday')
        result += self.line_of_table_row_pattern.format(self.line_of_table_row)
        return result

    def show_records(self, dict_of_records: dict) -> str:
        result = self.table_head()
        for indx, record in dict_of_records.items():
            result += self.table_row_pattern.format(indx, record.name.get_str(), record.phones[0].get_str(), record.email.get_str(), record.birthday.get_str())
            if len(record.phones) > 1:
                for phone in record.phones[1:]:
                    result += self.table_row_pattern.format('','', phone.get_str(), '', '',)
            result += self.line_of_table_row_pattern.format(self.line_of_table_row)
        return result
