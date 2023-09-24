# Identifier Class
from pandas import DataFrame
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error


class Ident:
    def __init__(self, mv=[], cv=[], metric='mse'):
        self.reg = None
        self.alpha = None
        self.beta = None
        self.gamma = None
        self.A = None
        
        self.mv = mv
        self.cv = cv
        self.n_mv = len(mv)
        
        self.na_best = 1
        self.nb_best = 1
        self.nk_best = 0
        self.e_best = 1e10
        
        self.metric = metric
        
        self.Y_pred = None
        
    def create_timeseries(self, df, na, nb, nk):
        CV = ['BP','P','SL','D','CP','D50']     #this is now different..... 

        X_df = DataFrame()
        for cv_i in self.cv:
            for i in range(na):
                X_df[[cv_i+'_%i' % (i+1)]] = df[[cv_i]].shift(i+1)

        for mv_i in self.mv:
            for j in range(nb):
                if mv_i in CV:
                    X_df[[mv_i+'_%i' % (j+nk)]] = df[[mv_i]].shift(j+nk+1)
                else:
                    X_df[[mv_i+'_%i' % (j+nk)]] = df[[mv_i]].shift(j+nk)
                
        X_df.fillna(method='bfill', inplace=True)
        X = X_df.to_numpy()

        try:
            Y_df = df[self.cv]
            Y = Y_df.to_numpy()
        except:
            Y = None
            
        return X, Y
        
    @staticmethod
    def train_test_split(X, Y, train_ratio=0.6, valid_ratio=0.2):
        
        n = len(X)
        n_split = int(train_ratio*n)
        n_split2 = n_split + int(valid_ratio*n)
        
        X_train = X[:n_split]
        X_valid = X[n_split:n_split2]
        
        
        Y_train = Y[:n_split]
        Y_valid = Y[n_split:n_split2]
        
        X_test = X[n_split2:]
        Y_test = Y[n_split2:]
 
        
        return X_train, X_valid, X_test, Y_train, Y_valid, Y_test # train, valid, test
    
    def identify(self, df, na=[2, 2], nb=[2,2], nk=[0,0]):
        df = df.copy()
        for na_i in range(na[0], na[1]+1):
            for nb_i in range(nb[0], nb[1]+1):
                for nk_i in range(nk[0], nk[1]+1):
                    X, Y = self.create_timeseries(df, na_i, nb_i, nk_i)
                    X_train, X_valid, X_test, Y_train, Y_valid, Y_test = self.train_test_split(X, Y)

                    reg = LinearRegression()
                    reg.fit(X_train, Y_train)

                    Y_pred = reg.predict(X_valid)

                    if self.metric.lower() == 'mse':
                        e = mean_squared_error(Y_valid, Y_pred)

                    elif self.metric.lower() == 'mae':
                        e = mean_absolute_error(Y_valid, Y_pred)

                    if e < self.e_best:
                        self.e_best = e.copy()
                        self.A = reg.coef_.copy().flatten()
                        self.gamma = reg.intercept_
                        self.na_best = na_i
                        self.nb_best = nb_i
                        self.nk_best = nk_i
                        Y_pred = reg.predict(X_test)
                        self.Y_pred = Y_pred.copy().flatten()
                        self.Y_real = Y_test.copy().flatten()
                        self.reg = reg
        
        if self.A is not None:
            ind = 0
            self.alpha = {}
            self.beta = {}
            
            for cv_i in self.cv:
                self.alpha[cv_i] = self.A[ind:ind+self.na_best]
                ind += self.na_best
            
            for mv_i in self.mv:
                self.beta[mv_i] = self.A[ind:ind+self.nb_best]
                ind += self.nb_best
            
            
    def predict(self, df):
        X, _ = self.create_timeseries(df, na=self.na_best, nb=self.nb_best, nk=self.nk_best)
        Y_pred = self.reg.predict(X)
        
        return Y_pred   