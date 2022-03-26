from googleapiclient.discovery import build
from google.oauth2 import service_account
import gspread
import pandas as pd
from gspread_formatting import *
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import get_as_dataframe, set_with_dataframe



class Spreadsheet_Manipulate():
    def __init__(self, spreadsheet_id):
        self.spreadsheet_id = spreadsheet_id

    def make_spreadsheet_format(self, worksheetName, array2D, appendNumber):
        """スプレッドシートのオブジェクトを取得する."""
        SCOPES = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        credentials = ServiceAccountCredentials.from_json_keyfile_name('./service-account.json', SCOPES)
        gc = gspread.authorize(credentials)

        workbook = gc.open_by_key(self.spreadsheet_id)

        worksheet_name = worksheetName
        try:
            workbook.add_worksheet(title=worksheet_name, rows=appendNumber, cols=10)
        except:
            pass

        update_ws = workbook.worksheet(worksheet_name)
        # Spreadsheetの背景の色を変える
        fmt = cellFormat(
            backgroundColor=color(1, 0.9, 0.9),
            horizontalAlignment='CENTER'
        )
        format_cell_range(update_ws, 'A1:J1', fmt)


        # 行列の作成
        cell_list = update_ws.get_all_values()
        # 行の数
        columns = len(cell_list) + 1

        ranges = '{0}!A{1}'.format(worksheet_name, columns)
        # print(ranges)
        workbook.values_update(ranges, params={'valueInputOption': 'USER_ENTERED'}, body={'values': array2D})


    def pd_change(self, worksheetName, dict_type, appendNumber):

        d2 = {}
        print('pd_change')
        # print(dict_type)


        for k,v in dict_type.items():   # 一度pd.Seriesに変換
            d2[k]=pd.Series(v)
        df=pd.DataFrame(d2)
        # df.to_csv("ロジオス.csv")
        # self.write_dataflame_in_spreadsheets(df, appendNumber, worksheetName)
        self.write_dataflame_in_spreadsheets(worksheetName, df, appendNumber)


    def write_dataflame_in_spreadsheets(self, worksheetName, dataframe, appendNumber):
        """スプレッドシートのオブジェクトを取得する."""
        SCOPES = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            r'./service-account.json', SCOPES
        )

        gc = gspread.authorize(credentials)

        # スプレットシートキーを指定してワークブックを選択を開く
        workbook = gc.open_by_key(self.spreadsheet_id)

        worksheet_name = worksheetName
        try:
            workbook.add_worksheet(title=worksheet_name, rows=appendNumber, cols=10)
        except:
            pass
        update_ws = workbook.worksheet(worksheet_name)
        # Spreadsheetの背景の色を変える
        fmt = cellFormat(
            backgroundColor=color(1, 0.9, 0.9),
            horizontalAlignment='CENTER'
        )
        format_cell_range(update_ws, 'A1:Z1', fmt)

        # 行列の作成
        cell_list = update_ws.get_all_values()
        # 行の数
        columns = len(cell_list) + 1

        ranges = '{0}!A{1}'.format(worksheet_name, columns)

        # 作ったDataFrameを貼り付ける。
        set_with_dataframe(update_ws, dataframe,
        resize=False, include_index=True)

