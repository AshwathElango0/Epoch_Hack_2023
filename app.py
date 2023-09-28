import pandas as pd                                                     #making necessary imports
from flask import Flask, request, url_for, render_template
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer=SentimentIntensityAnalyzer()                                       #initializations of variables, Flask, and reading database
dfj = pd.read_csv(r"C:\Users\Ashwath Elangovan\Desktop\Flask\movie_data_sheet_3.csv")
dfja = pd.read_csv(r"C:\Users\Ashwath Elangovan\Desktop\Flask\movie_data_sheet_3.csv")
app=Flask(__name__)

pos=0                                                                     
neg=0
neu=0
def polarity_finder(db):                                                  #Using an ML function to check polarity of comments
    x=db.iloc[-1, 2]
    data=analyzer.polarity_scores(x)
    return data

def review_tracker_jawan():                                                 #keeping track of sentiment for Jawan over time
    global pos, neg, neu, dfj
    l=len(dfj)
    sum=0
    for i in range(l):                                                      #finding average star rating
        data=dfj.iloc[i, 1]
        sum+=data
    avg=sum/l
    avg=round(avg, 2)
    for i in range(l):
        data=polarity_finder(dfj)
        if data['pos']>data['neg'] and data['pos']>data['neu']:
            pos+=1
        elif data['neg']>data['pos'] and data['neg']>data['neu']:
            neg+=1
        else:
            neu+=1
        if pos>neg and pos>neu:
            return f"POSITIVE REVIEWS! :) [Star rating : {avg}]"
        elif neg>pos and neg>neu:
            return f"Negative reviews so far :( [Star rating : {avg}]"
        else:
            return f"Neutral reviews so far :| [Star rating : {avg}]"

def review_tracker_jailer():                                                #keeping track of sentiment for Jailer over time
    global pos, neg, neu, dfa
    l=len(dfja)
    sum=0
    for i in range(l):                                                          #finding average star rating
        data=dfja.iloc[i, 1]
        sum+=data
    avg=sum/l
    avg=round(avg, 2)
    for i in range(l):
        data=polarity_finder(dfja)
        if data['pos']>data['neg'] and data['pos']>data['neu']:
            pos+=1
        elif data['neg']>data['pos'] and data['neg']>data['neu']:
            neg+=1
        else:
            neu+=1
        if pos>neg and pos>neu:
            return f"Positive reviews! :) [Star rating : {avg}]"
        elif neg>pos and neg>neu:
            return f"Negative reviews so far :( [Star rating : {avg}]"
        else:
            return f"Neutral reviews so far :| [Star rating : {avg}]"

@app.route('/')                                                         #home page
def home():
    text=review_tracker_jawan()
    text_2=review_tracker_jailer()
    return render_template('home.html', text=text, text_2=text_2)

@app.route('/movie_rev', methods=['POST'])                           
def movie_rev():
    if request.method=='POST':
        x=request.form
        if 'Jawan' in x:
            return render_template('jawan.html')
        if 'Jailer' in x:
            return render_template('jailer.html')
        
           
@app.route('/result_jawan', methods=['POST', 'GET'])
def result_jawan():
    global dfj
    if request.method=='POST':
        Rating=request.form['Rating']
        Review=request.form['Review']

        var=dfj.iloc[-1, 0]                                              #generating a review number to add user review to database
        var+=1

        df2=pd.DataFrame({'userID':var, 'Rating':float(Rating), 'Review':Review}, index=[0])       #adding user review to database
        df=pd.concat([dfj, df2], ignore_index=True)
        df.to_csv(r"C:\Users\Ashwath Elangovan\Desktop\Flask\movie_data_sheet_3.csv", index=False)

        data=polarity_finder(dfj)                                                                           #using ML to detect polarity scores
        if (data['compound']>0.65 and float(Rating)<3) or (data['compound']<0.3 and float(Rating)>4):    #removing contradicting comments
            df=df.drop(df.index[-1])
            df.to_csv(r"C:\Users\Ashwath Elangovan\Desktop\Flask\movie_data_sheet_3.csv", index=False)

        table=df.head()                                                                #showing user a few reviews
        t_ht=table.to_html(index=False)
    return render_template('jawan_result.html', t_ht=t_ht)                            #result page tells user their review is stored

@app.route('/result_jailer', methods=['POST', 'GET'])
def result_jailer():
    global dfja
    if request.method=='POST':
        Rating=request.form['Rating']
        Review=request.form['Review']

        var=dfja.iloc[-1, 0]                                              #generating a review number to add user review to database
        var+=1

        df2=pd.DataFrame({'userID':var, 'Rating':float(Rating), 'Review':Review}, index=[0])       #adding user review to database
        df=pd.concat([dfja, df2], ignore_index=True)
        df.to_csv(r"C:\Users\Ashwath Elangovan\Desktop\Flask\jailer_review.csv", index=False)

        data=polarity_finder(dfja)                                                                           #using ML to detect polarity scores
        if (data['compound']>0.65 and float(Rating)<3) or (data['compound']<0.3 and float(Rating)>4):    #removing contradicting comments
            df=df.drop(df.index[-1])
            df.to_csv(r"C:\Users\Ashwath Elangovan\Desktop\Flask\jailer_review.csv", index=False)

        table=df.head()
        t_ht=table.to_html(index=False)
    return render_template('jailer_result.html', t_ht=t_ht)

if __name__ == "__main__":
    app.run(debug=True) 


