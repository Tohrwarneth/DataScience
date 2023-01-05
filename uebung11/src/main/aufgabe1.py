import pandas as pd
import songlistrecommender as slr

desired_width = 320
pd.set_option('display.width', desired_width)

L = pd.read_csv('resources/songs.csv', sep='\t')
Lu = pd.read_csv('resources/users-songs.csv', sep='\t')

recommender = slr.SongListRecommender()

recommender.convert_data_frame(L)

for i in range(1, 16):
    print(recommender.recommend_song(L, Lu, i), '\n')
