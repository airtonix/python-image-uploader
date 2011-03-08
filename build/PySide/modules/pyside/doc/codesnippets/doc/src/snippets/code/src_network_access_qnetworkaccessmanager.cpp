//! [0]
manager = QNetworkAccessManager(self)
connect(manager, SIGNAL(finished("QNetworkReply*")),
        self, SLOT(replyFinished("QNetworkReply*")))

manager.get(QNetworkRequest(QUrl("http://qtsoftware.com")))
//! [0]


//! [1]
QNetworkRequest request
request.setUrl(QUrl("http://qtsoftware.com"))
request.setRawHeader("User-Agent", "MyOwnBrowser 1.0")

reply = manager.get(request)
connect(reply, SIGNAL("readyRead()"), self, SLOT("slotReadyRead()"))
connect(reply, SIGNAL(error("QNetworkReply.NetworkError")),
        self, SLOT(slotError("QNetworkReply.NetworkError")))
connect(reply, SIGNAL(sslErrors("QList<QSslError>")),
        self, SLOT(slotSslErrors("QList<QSslError>")))
//! [1]
