
import os
import researchpy as rp
from IPython.display import clear_output

desc_serv = {
            'beef': 'Weekly prices of different categories and qualities of beef and live animals per Member State and for the whole of the Union. More information can be found on the Info tab of the portal’s beef prices (carcasses) app and beef prices (live animals) app.',
            'pigmeat' : 'Weekly prices of different categories and qualities of pig meat as well as piglet prices per Member State and for the whole of the Union. More information can be found on the Info tab of the portal’s pigmeat carcasses prices app and piglet prices app and pigmeat cuts prices app.',
            'poultry' : 'Times series of average poultry prices per Member State and for the European Union with data from 1991. More information can be found on the Info tab of the portal’s poultry prices app and egg prices app.',
            'sheepAndGoat': 'Weekly prices for heavy and light lamb per Member State and weighted averages over the Union. More information can be found on the Info tab of the portal’s sheep and goat meat prices app.',
            'rawMilk': 'Weekly prices of raw milk as well as eight representative dairy products per Member State and weighted averages over the Union. More information can be found on the info tab of the portal’s raw milk prices and dairy prices apps.',
            'fruitAndVegetable' : 'Times series of average fruit and vegetables prices per Member State and for the European Union, showing prices in the full range from 2005. More information can be found on the Info tab of the portal’s fruit and vegetables prices app.',
            'cereal':'Prices of different kinds of cereals at a number of important EU markets, in different stages of the value chain (Free On Board, Departure from Silo etc.) as well as gross production, area and yield values by Member State. More information can be found on the Info tab of the portal’s cereals prices app and cereals production app.',
            'rice':'Weekly prices for different varieties of rice at different stages of the value chain in 7 producing Member States. More information can be found on the Info tab of the portal’s rice prices app.',
            'oilseeds':'Weekly oilseeds prices per Member State as well as weighted averages over the Union. More information can be found on the portal’s oilseeds prices app.',
            'sugar':'Evolution of 3 sugar region prices, with data series going back as far as January 2018. More information can be found on the portal’s sugar prices app.',
            'oliveOil':'Evolution of up to 7 different product categories in more than 20 different markets across the major oil-producing Member States, with some of the data series going back as far as June 2010. Annual and monthly gross production and end-of-year stocks of olive oil per Member State. More information can be found on the portal’s olive oil prices app and olive oil production app.',
            'wine': 'Prices of different classes of wine from France, Germany, Italy and Spain, with some of the time series ranging back to 2009. More information can be found on the Info tab of the portal’s wine prices app.'
            }

services ={'Beef':'beef',
           'Pigmeat':'pigmeat',
           'Eggs and Poultry' : 'poultry',
           'Sheep And Goat Meat' : 'sheepAndGoat',
           'Milk and dairy products' : 'rawMilk',
           'Fruit And Vegetables' : 'fruitAndVegetable',
           'Cereals' : 'cereal',
           'Rice' : 'rice',
           'Oilseeds' : 'oilseeds',
           'Sugar' : 'sugar',
           'Olive oil' : 'oliveOil',
           'Wine' : 'wine'}


serv = list(services.keys())

countries = {'Austria' : 'AT',
             'Bulgaria':'BG',
             'Cyprus':'CY',
             'Czechia':'CZ',
             'Denmark':'DK',
             'Finland':'FI',
             'France':'FR',
             'Germany':'DE',
             'Hungary':'HU',
             'Ireland':'IE',
             'Italy':'IT',
             'Latvia':'LV',
             'Netherlands':'NL',
             'Poland':'PL',
             'Portugal':'PT',
             'Romania':'RO',
             'Spain':'ES',
             'Sweden':'SE'}


def Plot_box(df, y, x, color, title, xaxis_title_text, yaxis_title_text, legend_title_text):
    fig = px.box(df,
                 y= y, 
                 x= x, 
                 orientation='v', 
                 color= color,
                 notched=True)

    fig.update_layout(
        showlegend=True,
        title_text=title,
        title_font_color='#333333',
        #width = 1200,
        #height=500,
        plot_bgcolor='white',
        xaxis_title_font_color='grey',
        yaxis_title_font_color='grey',
        yaxis_color='grey',
        xaxis_color='grey',
        xaxis_title_text = xaxis_title_text,
        yaxis_title_text = yaxis_title_text,
        xaxis_gridcolor = '#F7FCF0',
        xaxis_linecolor = '#F7FCF0',
        coloraxis_showscale=False,
        legend_title_text= legend_title_text)

    fig.update_xaxes(categoryorder='total descending')
    
    return fig



def get_statistics(df, stats_by, column_value):
    filters = df[f'{stats_by}'].unique()
    dataframe = pd.DataFrame()
    
    for f in range(len(filters)):
  
        if f == filters[0]:
            dataframe = rp.summarize(df[df[f'{stats_by}'] == filters[f]][f'{column_value}'])
            #rp.summary_cont(df[df[f'{stats_by}'] == filters[f]][f'{column_value}'])
            dataframe.loc[f,f'{stats_by}'] = filters[f]
        else:
            data = rp.summarize(df[df[f'{stats_by}'] == filters[f]][f'{column_value}'])
            data.loc[0,f'{stats_by}'] = filters[f]
            dataframe = pd.concat([dataframe,data])
            dataframe = dataframe.reset_index(drop=True)
            
        #getting others statics data
        d = df[df[f'{stats_by}'] == filters[f]][f'{column_value}'].describe()
        dataframe.loc[f,'min'] = d[3]
        dataframe.loc[f,'25%'] = d[4]
        dataframe.loc[f,'50%'] = d[5]
        dataframe.loc[f,'75%'] = d[6]
        dataframe.loc[f,'max'] = d[7]
        dataframe.loc[f,'range'] = d[7] - d[3]
        dataframe.loc[f,'kurtosis'] = df[df[f'{stats_by}'] == filters[f]][f'{column_value}'].kurtosis()
        dataframe.loc[f,'skew'] = df[df[f'{stats_by}'] == filters[f]][f'{column_value}'].skew()
    
    
    dataframe[['N', 'Mean', 'Median', 'Variance', 'SD', 'SE']] = dataframe[['N', 'Mean', 'Median', 'Variance', 'SD', 'SE']]\
        .apply(pd.to_numeric)
    
    clear_output()
    return dataframe

def Plot_line(df_stat, x, title, xaxis_title_text = '', yaxis_title_text = '', y='Mean'):

    fig = px.line(df_stat,
                 y= y, 
                 x= x,
                 text = df_stat[y].map('{:,.2f}'.format))


    fig.update_layout(
        showlegend=True,
        title_text=title,
        title_font_color='#333333',
        #width = 1200,
        #height=500,
        plot_bgcolor='white',
        xaxis_title_font_color='grey',
        yaxis_title_font_color='grey',
        yaxis_color='grey',
        xaxis_color='grey',
        xaxis_title_text = xaxis_title_text,
        yaxis_title_text = yaxis_title_text,
        yaxis_gridcolor = '#F7FCF0',
        coloraxis_showscale=False,
        legend_title_text= "",
        margin_t=90,
        margin_b=10)


    fig.update_xaxes(categoryorder='total descending')

    fig.update_traces(textfont_size=10, textposition='top center')
    
    return fig

def get_prices(service, state):
    url = f'https://ec.europa.eu/agrifood/api/{service}/prices?memberStateCodes={state}&beginDate=01/01/2022&endDate=31/12/2022'
    file_name = f'{service}_{state}.bz2'
   

    if os.path.exists(file_name) == False: #First checking if database exists
        print(f'Getting Data...')    
    
        try:
            ind = pd.read_json(url)
        except:
            print(f'We got an Error getting data from API')

        ind.to_csv(file_name, index=False,compression='bz2') #Saving Data
        print(f'File saved as {file_name}')    
    
    else:
        print(f'Reading {file_name}')
        ind = pd.read_csv(file_name) #if exists it'll just read the data        
    
    print(f'DataFrame with {len(ind):,} observations and {len(ind.columns)} features available')
    
    return ind


def make_card (name, symbol, change, value):
    color = "danger" if change > 0 else "success"
    icon = f"bi bi-arrow-down text-{color}" if change < 0 else f"bi bi-arrow-up text-{color}"
    border = f"border-start border-{color} border-5"
    return dbc.Card(
                    dbc.CardBody(
                        [
                            html.H1([html.I(className=symbol), name], className="text-nowrap"),
                            html.H3(f"{value}"),
                            html.Div(
                                [
                                    html.I(f"{change:,.2%}", className=icon),
                                    "",
                                ]
                            ),
                        ], className= border
                    ),
        style={"width": "18rem"},
        className="text-center m-4 my-4"
    )
