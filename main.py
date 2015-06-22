#coding: utf-8
import pygtk
import gtk
import tweepy

consumer_key = '********'
consumer_secret = '********'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.secure = True

user_id = raw_input('ユーザー名を入力してください: ')

judge = False

file = open('oauth.txt', 'r')

for line in file:
    parts = line.rstrip('\n').split(' ')
    if parts[0] == user_id:
        judge = True
        access_token = parts[1]
        access_token_secret = parts[2]
        auth.set_access_token(access_token, access_token_secret)
        break

file.close()
file = open('oauth.txt', 'a+')
        
if judge == False:
    try:
        url = auth.get_authorization_url()
        print 'このURLにアクセスして、アプリ連携してください: ' + url
    except tweepy.TweepError:
        print 'エラー'

    code = raw_input('認証コード: ')

    auth.secure = True
    auth.get_access_token(code)
    access_token = auth.access_token.key
    access_token_secret = auth.access_token.secret
    auth.set_access_token(access_token, access_token_secret)

    line = user_id + ' ' + access_token + ' ' + access_token_secret + '\n'
    file.write(line)

file.close()

global api
api = tweepy.API(auth)

global reply_to
reply_to = None

class App:
    def __init__(self):
        self.window = gtk.Window()
        self.window.set_title('hideous')
        self.window.show()

        self.all_box = gtk.VBox()

        # 一番上のHBox
        self.me_box = gtk.HBox()

        self.me_label = gtk.Label()
        self.my_name = api.me().name
        self.my_screen_name = api.me().screen_name
        self.me_label.set_text(self.my_name + '(' + self.my_screen_name + ')')

        self.entry = gtk.Entry()
        self.entry.set_max_length(140)

        self.tweet_button = gtk.Button()
        self.tweet_button.set_label('Tweet')
        self.tweet_button.connect('clicked', self.tweet)

        self.me_box.add(self.me_label)
        self.me_box.add(self.entry)
        self.me_box.add(self.tweet_button)

        self.all_box.add(self.me_box)
        
        #TLの各ツイートに対するVBox(複数)
        self.tl_box = []
        self.tl = api.home_timeline(count=5)

        self.one_label = []
        self.ones_name = []
        self.ones_screen_name = []
        self.ones_tweet = []
        for i in range(5):
            self.one_label.append(gtk.Label())
            self.ones_name.append(self.tl[i].user.name)
            self.ones_screen_name.append(self.tl[i].user.screen_name)
            self.one_label[i].set_text(self.ones_name[i] + '(' + self.ones_screen_name[i] + ')')

            self.ones_tweet.append(gtk.Label())
            self.ones_tweet[i].set_text(self.tl[i].text)

            self.reply_button = gtk.Button()
            self.reply_button.set_label('Reply')
            self.reply_button.connect('clicked', self.reply, self.tl[i].id)

            self.rt_button = gtk.Button()
            self.rt_button.set_label('RT')
            self.rt_button.connect('clicked', self.retweet, self.tl[i].id)

            self.fav_button = gtk.Button()
            self.fav_button.set_label('Fav')
            self.fav_button.connect('clicked', self.fav, self.tl[i].id)

            self.action_box = gtk.VBox()
            self.action_box.add(self.reply_button)
            self.action_box.add(self.rt_button)
            self.action_box.add(self.fav_button)

            self.tl_box.append(gtk.HBox())
            self.tl_box[i].add(self.one_label[i])
            self.tl_box[i].add(self.ones_tweet[i])
            self.tl_box[i].add(self.action_box)
            self.all_box.add(self.tl_box[i])

        self.window.add(self.all_box)
        self.window.show_all()
        
    def tweet(self, widget):
        self.tweet = self.entry.get_text()
        if reply_to == None:
            api.update_status(self.tweet)
        elif reply_to.user.screen_name in tweet:
            api.update_status(self.tweet in_reply_to_status_id=reply_to)
        else:
            api.update_status(self.tweet)
        self.entry.set_text('')

    def reply(self, widget, tweet_id):
        self.entry.set_text('@' + tweet_id.user.screen_name)
        reply_to = tweet_id

    def retweet(self, widget, tweet_id):
        api.retweet(tweet_id)
        
    def fav(self, widget, tweet_id):
        api.create_favorite(tweet_id)

    def main(self):
        gtk.main()

if __name__ == '__main__':
    app = App()
    app.main()