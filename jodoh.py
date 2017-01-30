import numpy as np

artiscewek = ['Raisa','Isyana Sarasvati','Ariel Tatum','Jessica Mila','Maudy Ayunda','Yuki Kato','Park Shin Hye','Chelsea Islan','Prilly    Latuconsina','Chef Marinka','Dinda Kirana','Kimberly Ryder','Pevita Pearce','Raline Shah','Pamela Bowie','Velove Vexia']
artiscowok = ['Lee Min Ho','Mario Maurer', 'Al Ghazali','Andika Kangen Band','Stefan William','Aliando Syarief','Jhonn Tea','Teuku Rassya']

def entropy(omom):
    arr = [0]
    arr = np.array(arr, dtype=np.int64)
    nama = [ord(x) for x in omom.upper()]
    for i in np.arange(0, 256):
        nl = np.sum(nama == i)
        # print nl
        if nl == 0:
            continue
        t = len(nama)
        pl = float(nl)/float(t)
        # print pl
        x = pl*np.log2(1/pl)
        arr = np.append(arr, x)
    return arr.sum()

def terdekat(e1,artis):
    dekat = 0
    selisih = abs(e1-artis[0])
    for i in artis:
        selisih2 = abs(e1-i)
        if selisih2<selisih:
            selisih = selisih2
            dekat = artis.index(i)
    return dekat

entropyartiscewek = [entropy(x) for x in artiscewek]
entropyartiscowok = [entropy(x) for x in artiscowok]

Mirip = 'Tidak Ada'

nama = raw_input('Masukkan Nama Anda : ')
jk = raw_input('Masukkan Jenis Kelamin : ')
if jk.lower() == 'l':
    mirip = artiscewek[terdekat(entropy(nama),entropyartiscewek)]
else:
    mirip = artiscowok[terdekat(entropy(nama),entropyartiscowok)]

print 'Jodoh kamu adalah:', mirip
