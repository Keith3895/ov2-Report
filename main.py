import numpy as nup
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
class Main:
    
    def __init__(self):
        self.loadCSV()
        self.__drawClosure()
        self.__drawseverity()
        self.__drawTotalCount()

        # dates = pd.date_range(start='29/01/2020 11:54:12',end='24/04/2020 13:14:46')
        # bug.to_csv('out.csv', index=False)
    
    def loadCSV(self):
        self.csvContent = pd.read_csv('new2.csv')
    
    def loadBugs(self):
        return self.csvContent.loc[self.csvContent['Work_Item_Type'] == 'Bug']
    
    def getByProjectName(self,df,projectName):
        df = df.loc[df['Team_Project'] == projectName]
        df['Resolved_Date'] = pd.to_datetime(df['Resolved_Date'],format="%d/%m/%Y %H:%M:%S")
        df['Created_Date'] = pd.to_datetime(df['Created_Date'],format="%d/%m/%Y %H:%M:%S")
        df['closure'] = (df['Resolved_Date'] - df['Created_Date']).dt.days
        df['closure'][df['closure'] < 0] = nup.nan
        df.dropna(subset = ["closure",'Severity'], inplace=True)
        return df
   
    def drawHist(self, projectName,column):
        bug = self.loadBugs()
        bug = self.getByProjectName(bug,projectName)
        return go.Histogram(histfunc="count",  x=bug[column], name=projectName)
    
    def __drawClosure(self):
        projects = ['Document Management System','OV2','Starch Mapping','Customer Engagement Tools','LOTO']
        fig= go.Figure()
        for i in projects:
            fig.add_trace(self.drawHist(i,'closure'))

        fig.update_layout(
            title_text='Closure of bugs by Number of days', # title of plot
            xaxis_title_text='Number of Days', # xaxis label
            yaxis_title_text='Number of Bugs', # yaxis label
            bargap=0.2, # gap between bars of adjacent location coordinates
            bargroupgap=0.1 # gap between bars of the same location coordinates
        )
        # fig.update_layout(barmode='stack')
        fig.show()
        pio.write_html(fig, file='closure.html', auto_open=True)
    
    def __drawseverity(self):
        projects = ['Document Management System','OV2','Starch Mapping','Customer Engagement Tools','LOTO']
        fig= go.Figure()
        for i in projects:
            fig.add_trace(self.drawHist(i,'Severity'))
        fig.update_layout(
            title_text='Number of Bugs By Severity', # title of plot
            xaxis_title_text='Severity', # xaxis label
            yaxis_title_text='Number of Bugs', # yaxis label
            bargap=0.2, # gap between bars of adjacent location coordinates
            bargroupgap=0.1 # gap between bars of the same location coordinates
        )
        fig.show()
        pio.write_html(fig, file='Severity.html', auto_open=True)
    
    def __drawTotalCount(self):
        self.csvContent.dropna(subset = ['Severity'], inplace=True)
        fig = px.histogram(self.csvContent, y="Team_Project", histfunc='count',
        title='Total number of bugs by project')
        fig.show()
        pio.write_html(fig, file='TotalCount.html', auto_open=True)
Main()