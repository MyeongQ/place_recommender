import torch
import pandas as pd
import torch.nn.functional as F
import torch.nn
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split


class MatrixFactorization():
    def __init__(self, R, k=12, learning_rate=0.1, epochs=100, lambda1=0.0001, lambda2=0.0001, lambda3=0.001, lambda4=0.001):
        """
        :param R: rating matrix
        :param k: latent parameter = Rank
        :param learning_rate: alpha on weight update
        :param reg_param: beta on weight update
        :param epochs: training epochs
        """

        self._R = R
        self._num_users, self._num_items = R.shape
        self._k = k
        self._learning_rate = learning_rate
        self._epochs = epochs

        # Global Baseline Estimate 적용시 bias_item, bias_user, Pi, Qx를 정규화하기 위해 사용
        self._lambda1 = lambda1
        self._lambda2 = lambda2
        self._lambda3 = lambda3
        self._lambda4 = lambda4

        self._place_list = sorted(list(set(self._R['placeID'])))
        self._user_list = sorted(list(set(self._R['userID'])))
        # print(user_list)
        # print(test)

    def fit(self):
        # train / test set 나누기
        train, test = train_test_split(self._R, test_size=0.1, random_state=0)
        print(train.shape, test.shape)

        places_train = train['placeID'].map(lambda x: self._place_list.index(x))
        users_train = train['userID'].map(lambda x: self._user_list.index(x))
        ratings_train = train['rating']
        places_test = test['placeID'].map(lambda x: self._place_list.index(x))
        users_test = test['userID'].map(lambda x: self._user_list.index(x))
        ratings_test = test['rating']

        self._places_train = torch.LongTensor(places_train.values)
        self._users_train = torch.LongTensor(users_train.values)
        self._ratings_train = torch.FloatTensor(ratings_train.values)
        self._places_test = torch.LongTensor(places_test.values)
        self._users_test = torch.LongTensor(users_test.values)
        self._ratings_test = torch.FloatTensor(ratings_test.values)

        #rank = 12
        numPlaces = len(list(set(self._place_list)))
        numUsers = len(list(set(self._user_list)))
        print(numPlaces,numUsers)

        # init latent features
        # rank → 사용자, 아이템 vector의 차원
        # numUsers → 사용자 수
        # numItems → 아이템 수
        # P → 아이템 매트릭스
        # Q → 사용자매트릭스
        self._P = torch.randn(numPlaces, self._k, requires_grad=True)
        self._Q = torch.randn(numUsers, self._k, requires_grad=True)

        # 전체 평점 평균 (Global Baseline Estimate를 적용한 Latent Factor model의 가설함수에 필요)
        self._m = (ratings_train.sum() / len(ratings_train)).item()

        # 각 item, user 벡터에 적용할 bias 값
        # 학습해야하는 파라미터이기에 랜덤한 값으로 채워넣는다.
        self._b_p = torch.randn(numPlaces, requires_grad=True)
        self._b_u = torch.randn(numUsers, requires_grad=True)

        # training 시작
        self._X = []
        self._Y = []
        self._Y_predict = []

        optimizer = torch.optim.Adam([self._P, self._Q, self._b_p, self._b_u], lr=self._learning_rate)
        for epoch in range(self._epochs):
            hypothesis = self.hypothesis_score(self._places_train, self._users_train)
            cost = F.mse_loss(hypothesis, self._ratings_train)
            loss = self.cost(hypothesis, self._ratings_train)

            # 기울기 계산
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            # 기울기 계산 필요 없다.
            with torch.no_grad():
                hypo_test = self.hypothesis_score(self._places_test, self._users_test)
                cost_test = F.mse_loss(hypo_test, self._ratings_test)

                # cost 결과 작성
                self._X.append(epoch)
                self._Y.append(float(cost))
                self._Y_predict.append(cost_test)

                if epoch % 50 == 0:
                    print("epoch: {}, cost: {:.6f}".format(epoch, cost.item()))

    def hypothesis_score(self, places, users):
        # 가설 = 예상별점(아이템벡터와 유저벡터 내적) + 전체평점평균 + 아이템벡터의 bias + 유저벡터의 bias
        hypothesis = torch.sum(self._P[places].float() * self._Q[users].float(), dim=1, dtype=torch.float32) \
                    + self._m + self._b_p[places] + self._b_u[users]
        return hypothesis

    def cost(self, hypothesis, ratings):
        # loss = MSE + 정규화
        cost = F.mse_loss(hypothesis, ratings)
        loss = cost + self._lambda1 * torch.sum(self._P**2, dtype=torch.float32)\
               + self._lambda2 * torch.sum(self._Q**2, dtype=torch.float32)\
               + self._lambda3 * torch.sum(self._b_p**2, dtype=torch.float32)\
               + self._lambda4 * torch.sum(self._b_u**2, dtype=torch.float32)
        return loss

    def show_result(self):
        print("X: ", self._X)
        print("Y: ", self._Y)
        plt.ylabel("MSE")
        plt.xlabel("Epoch")
        plt.plot(self._X, self._Y, c="blue", label="Training MSE")
        plt.plot(self._X, self._Y_predict, c="red", label="Test MSE")
        plt.legend()
        print("final error=", self._Y_predict[-1])
        plt.show()

    # P-item, Q-user, bias_item, bias_user
    def recommend_places(self, userID, maximum=20, threshold=3.5, visited=[]):
        userIdx = self._user_list.index(userID)
        recom_places = []
        for i in range(len(self._place_list)):  # i=placeIdx
            placeID = self._place_list[i]
            if placeID in visited: continue
            predict_score = float(torch.sum(self._P[i] * self._Q[userIdx]) + self._m + self._b_p[i] + self._b_u[userIdx])
            if predict_score >= threshold:
                recom_places.append((placeID, predict_score))

        recom_places.sort(key=lambda x: -x[1])
        if len(recom_places) > maximum:
            recom_places = recom_places[:maximum]
        return recom_places


if __name__ == "__main__":
    # 1차 전처리된 csv파일
    PATH = "../dataset/user-movie-ratings.csv"
    rating = pd.read_csv(PATH, sep=",", names=['placeID', 'userID', 'rating'])[1:]
    print(rating)

    recommender = MatrixFactorization(R=rating, k=15)
    recommender.fit()
    recommender.show_result()
    print(recommender.recommend_places(userID=2, maximum=15, threshold=3.5, visited=[0, 1, 2, 8, 21, 24, 26, 30, 37, 73]))
