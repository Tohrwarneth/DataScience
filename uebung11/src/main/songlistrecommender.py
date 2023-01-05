import numpy as np
import pandas as pd


class SongListRecommender:

    def convert_data_frame(self, df: pd.DataFrame):
        classic = list()
        metal = list()
        barock = list()
        pop = list()
        dreiertakt = list()
        tonart = list()
        jahre = list()
        laenge = list()
        geschlecht = list()
        tempo = list()

        minimum_jahr = np.min(df.JAHR)
        maximum_jahr = np.max(df.JAHR)

        for length in df.LAENGE:
            temp = length.split(':')
            laenge.append(int(temp[0]) * 60 + int(temp[1]))

        minimum_laenge = np.min(laenge)
        maximum_laenge = np.max(laenge)

        minimum_tempo = np.min(df.TEMPO)
        maximum_tempo = np.max(df.TEMPO)

        for index in df.index:
            classic.append(1 if df['GENRE'][index] == 'Klassik' else 0)
            metal.append(1 if df['GENRE'][index] == 'Metal' else 0)
            barock.append(1 if df['GENRE'][index] == 'Barock' else 0)
            pop.append(1 if df['GENRE'][index] == 'Pop' else 0)

            dreiertakt.append(1 if int(df['RHYTHMUS'][index].split('/')[0]) % 3 == 0 else 0)

            temp = df['TONART'][index].replace('s', '')
            tonart.append(((ord(temp) - 64) - 1) / 7)  # 64 für start von groß A und -1 um bei 0 zu starten

            temp = df['JAHR'][index]
            jahre.append((temp - minimum_jahr) / (maximum_jahr - minimum_jahr))

            temp = laenge[index]
            laenge[index] = (temp - minimum_laenge) / (maximum_laenge - minimum_laenge)

            geschlecht.append(1 if df['TONGESCHLECHT'][index] == 'Dur' else 0)

            temp = df['TEMPO'][index]
            tempo.append((temp - minimum_tempo) / (maximum_tempo - minimum_tempo))

        df['KLASSIK'] = classic
        df['METAL'] = metal
        df['BAROCK'] = barock
        df['POP'] = pop
        df['DREIERTAKT'] = dreiertakt
        df['TONART'] = tonart
        df['JAHR'] = jahre
        df['LAENGE'] = laenge
        df['TONGESCHLECHT'] = geschlecht
        df['TEMPO'] = tempo

    def recommend_song(self, L: pd.DataFrame, Lu: pd.DataFrame, user: int):
        Lu = Lu[Lu.USER == user]
        if (len(Lu) == 0):
            return 'No user'

        temp = list()
        for l in Lu.SONG:
            temp.append(L[L.ID == l])

        df = pd.concat(temp)
        yJahr = np.median(df.JAHR)
        yTonart = np.median(df.TONART)
        yKlassik = np.median(df.KLASSIK)
        yMetal = np.median(df.METAL)
        yBarock = np.median(df.BAROCK)
        yPop = np.median(df.POP)
        yDreitakt = np.median(df.DREIERTAKT)
        yTempo = np.median(df.TEMPO)
        yLaenge = np.median(df.LAENGE)
        yGeschlecht = np.median(df.TONGESCHLECHT)
        y = np.array([yJahr, yTonart, yKlassik, yMetal, yBarock, yPop, yDreitakt, yTempo, yLaenge, yGeschlecht])
        yNorm = self.norm(y)

        L = pd.merge(L, df, indicator=True, how='outer').query('_merge=="left_only"').drop('_merge', axis=1)
        dl = -1
        song = ''
        for index in L.index:
            xJahr = np.median(L.JAHR[index])
            xTonart = np.median(L.TONART[index])
            xKlassik = np.median(L.KLASSIK[index])
            xMetal = np.median(L.METAL[index])
            xBarock = np.median(L.BAROCK[index])
            xPop = np.median(L.POP[index])
            xDreitakt = np.median(L.DREIERTAKT[index])
            xTempo = np.median(L.TEMPO[index])
            xLaenge = np.median(L.LAENGE[index])
            xGeschlecht = np.median(L.TONGESCHLECHT[index])
            x = np.array([xJahr, xTonart, xKlassik, xMetal, xBarock, xPop, xDreitakt, xTempo, xLaenge, xGeschlecht])
            xNorm = self.norm(x)
            temp = (x.dot(y) / (xNorm * yNorm))
            if (dl == -1) or (temp < dl):
                dl = temp
                song = L.TITEL[index]

        if (song == ''):
            return 'Kein Lied zum empfehlen'
        return 'user: ' + str(user) + '\nLied: ' + song

    def norm(self, vector):
        temp = 0
        for i in vector:
            temp = temp + (i * i)
        return np.sqrt(temp)
