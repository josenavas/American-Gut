#!/usr/bin/env python

from __future__ import division
from unittest import TestCase, main

import numpy as np
import numpy.testing as npt
import skbio

from os import rmdir
from os.path import realpath, dirname, join as pjoin, exists
from pandas import Series, DataFrame, Index
from pandas.util.testing import assert_index_equal, assert_frame_equal
from americangut.diversity_analysis import (pad_index,
                                            check_dir,
                                            post_hoc_pandas,
                                            multiple_correct_post_hoc,
                                            get_distance_vectors,
                                            segment_colormap,
                                            _get_bar_height,
                                            _get_p_value,
                                            _correct_p_value,
                                            split_taxa,
                                            get_ratio_heatmap)

__author__ = "Justine Debelius"
__copyright__ = "Copyright 2014"
__credits__ = ["Justine Debelius"]
__license__ = "BSD"
__version__ = "unversioned"
__maintainer__ = "Justine Debelius"
__email__ = "Justine.Debelius@colorado.edu"

# Determines the location fo the reference files
TEST_DIR = dirname(realpath(__file__))


class DiversityAnalysisTest(TestCase):

    def setUp(self):
        # Sets up lists for the data frame
        self.ids = ['000001181.5654', '000001096.8485', '000001348.2238',
                    '000001239.2471', '000001925.5603', '000001098.6354',
                    '000001577.8059', '000001778.097' ,  '000001969.1967',
                    '000001423.7093', '000001180.1049', '000001212.5887',
                    '000001984.9281', '000001025.9349', '000001464.5884',
                    '000001800.6787', '000001629.5398',  '000001473.443',
                    '000001351.1149', '000001223.1658', '000001884.0338',
                    '000001431.6762', '000001436.0807', '000001726.2609',
                    '000001717.784' , '000001290.9612', '000001806.4843',
                    '000001490.0658', '000001719.4572', '000001244.6229',
                    '000001092.3014', '000001315.8661', '000001525.8659',
                    '000001864.7889', '000001816.9'   , '000001916.7858',
                    '000001261.3164', '000001593.2364', '000001817.3052',
                    '000001879.8596', '000001509.217' , '000001658.4638',
                    '000001741.9117', '000001940.457' , '000001620.315' ,
                    '000001706.6473', '000001287.1914', '000001370.8878',
                    '000001943.0664', '000001187.2735', '000001065.4497',
                    '000001598.6903', '000001254.2929', '000001526.143' ,
                    '000001980.8969', '000001147.6823', '000001745.3174',
                    '000001978.6417', '000001547.4582', '000001649.7564',
                    '000001752.3511', '000001231.5535', '000001875.7213',
                    '000001247.5567', '000001412.7777', '000001364.1045',
                    '000001124.3191', '000001654.0339', '000001795.4842',
                    '000001069.8469', '000001149.2945', '000001858.8903',
                    '000001667.8228', '000001648.5881', '000001775.0501',
                    '000001023.1689', '000001001.0859', '000001129.0853',
                    '000001992.9674', '000001174.3727', '000001126.3446',
                    '000001553.099' , '000001700.7898', '000001345.5369',
                    '000001821.4033', '000001921.0702', '000001368.0382',
                    '000001589.0756', '000001428.6135', '000001417.7107',
                    '000001050.2949', '000001549.0374', '000001169.7575',
                    '000001827.0751', '000001974.5358', '000001081.3137',
                    '000001452.7866', '000001194.8171', '000001781.3765',
                    '000001676.7693', '000001536.9816', '000001123.9341',
                    '000001950.0472', '000001386.1622', '000001789.8068',
                    '000001434.209',  '000001156.782' , '000001630.8111',
                    '000001930.9789', '000001136.2997', '000001901.1578',
                    '000001358.6365', '000001834.4873', '000001175.739' ,
                    '000001565.3199', '000001532.5022', '000001844.4434',
                    '000001374.6652', '000001066.9395', '000001277.3526',
                    '000001765.7054', '000001195.7903', '000001403.1857',
                    '000001267.8034', '000001463.8063', '000001567.256' ,
                    '000001986.3291', '000001912.5336', '000001179.8083',
                    '000001539.4475', '000001702.7498', '000001362.2036',
                    '000001605.3957', '000001966.5905', '000001690.2717',
                    '000001796.78'  , '000001965.9646', '000001570.6394',
                    '000001344.0749', '000001505.094' , '000001500.3763',
                    '000001887.334' , '000001896.9071', '000001061.5473',
                    '000001210.8434', '000001762.6421', '000001389.9375',
                    '000001747.7094', '000001275.7608', '000001100.6327',
                    '000001832.2851', '000001627.4754', '000001811.8183',
                    '000001202.8991', '000001163.3137', '000001196.7148',
                    '000001318.8771', '000001155.3022', '000001724.2977',
                    '000001737.328' , '000001289.1381', '000001480.495',
                    '000001797.7651', '000001117.9836', '000001108.0792',
                    '000001060.2191', '000001379.0706', '000001513.9224',
                    '000001731.9258', '000001563.7487', '000001988.1656',
                    '000001594.7285', '000001909.1042', '000001920.0818',
                    '000001999.9644', '000001133.9942', '000001608.1459',
                    '000001784.159' , '000001543.759' , '000001669.3403',
                    '000001545.3456', '000001177.5607', '000001387.8614',
                    '000001086.4642', '000001514.2136', '000001329.4163',
                    '000001757.7272', '000001574.9939', '000001750.1329',
                    '000001682.8423', '000001331.238' , '000001330.6685',
                    '000001556.6615', '000001575.4633', '000001754.591' ,
                    '000001456.5672', '000001707.2857', '000001164.864' ,
                    '000001466.7766', '000001383.5692', '000001911.8425',
                    '000001880.6072', '000001278.4999', '000001671.8068',
                    '000001301.3063', '000001071.2867', '000001192.7655',
                    '000001954.0541', '000001041.0466', '000001862.7417',
                    '000001587.4996', '000001242.6044', '000001040.399' ,
                    '000001744.3975', '000001189.5132', '000001885.0033',
                    '000001193.7964', '000001204.533' , '000001279.8583',
                    '000001488.2298', '000001971.1838', '000001492.0943',
                    '000001722.285' , '000001947.5481', '000001054.343' ,
                    '000001227.5756', '000001603.0731', '000001948.0095',
                    '000001393.6518', '000001661.6287', '000001829.9104',
                    '000001342.3216', '000001341.7147', '000001994.1765',
                    '000001400.0325', '000001324.5159', '000001355.789' ,
                    '000001538.6368', '000001121.0767', '000001377.1835',
                    '000001831.3158', '000001968.0205', '000001003.7916',
                    '000001502.0367', '000001729.5203', '000001284.1266',
                    '000001252.1786', '000001533.2349', '000001198.741' ,
                    '000001483.1918', '000001528.3996', '000001304.2649',
                    '000001281.7718', '000001441.8902', '000001203.4813',
                    '000001657.915' , '000001668.1396', '000001560.6021',
                    '000001213.1081', '000001894.5208', '000001791.9156',
                    '000001371.9864', '000001631.1904', '000001635.3301',
                    '000001541.2899', '000001748.311' , '000001326.0745',
                    '000001736.2491', '000001028.1898', '000001997.5772',
                    '000001764.9201', '000001664.4968', '000001031.0638',
                    '000001457.8448', '000001335.8157', '000001053.361' ,
                    '000001372.2917', '000001847.3652', '000001746.7838',
                    '000001173.0655', '000001653.9771', '000001104.8455',
                    '000001642.548' , '000001866.4881', '000001381.5643',
                    '000001673.6333', '000001839.2794', '000001855.195' ,
                    '000001698.1673', '000001813.0695', '000001153.6346',
                    '000001354.0321', '000001035.5915', '000001469.6652',
                    '000001422.9333', '000001148.4367', '000001551.0986',
                    '000001047.9434', '000001160.0422', '000001621.3736']
        self.raw_ids = ['1181.5654', '1096.8485', '1348.2238', '1239.2471',
                        '1925.5603', '1098.6354', '1577.8059', '1778.097',
                        '1969.1967', '1423.7093', '1180.1049', '1212.5887',
                        '1984.9281', '1025.9349', '1464.5884', '1800.6787',
                        '1629.5398', '1473.443', '1351.1149', '1223.1658',
                        '1884.0338', '1431.6762', '1436.0807', '1726.2609',
                        '1717.784', '1290.9612', '1806.4843', '1490.0658',
                        '1719.4572', '1244.6229', '1092.3014', '1315.8661',
                        '1525.8659', '1864.7889', '1816.9', '1916.7858',
                        '1261.3164', '1593.2364', '1817.3052', '1879.8596',
                        '1509.217', '1658.4638', '1741.9117', '1940.457',
                        '1620.315', '1706.6473', '1287.1914', '1370.8878',
                        '1943.0664', '1187.2735', '1065.4497', '1598.6903',
                        '1254.2929', '1526.143', '1980.8969', '1147.6823',
                        '1745.3174', '1978.6417', '1547.4582', '1649.7564',
                        '1752.3511', '1231.5535', '1875.7213', '1247.5567',
                        '1412.7777', '1364.1045', '1124.3191', '1654.0339',
                        '1795.4842', '1069.8469', '1149.2945', '1858.8903',
                        '1667.8228', '1648.5881', '1775.0501', '1023.1689',
                        '1001.0859', '1129.0853', '1992.9674', '1174.3727',
                        '1126.3446', '1553.099', '1700.7898', '1345.5369',
                        '1821.4033', '1921.0702', '1368.0382', '1589.0756',
                        '1428.6135', '1417.7107', '1050.2949', '1549.0374',
                        '1169.7575', '1827.0751', '1974.5358', '1081.3137',
                        '1452.7866', '1194.8171', '1781.3765', '1676.7693',
                        '1536.9816', '1123.9341', '1950.0472', '1386.1622',
                        '1789.8068', '1434.209', '1156.782', '1630.8111',
                        '1930.9789', '1136.2997', '1901.1578', '1358.6365',
                        '1834.4873', '1175.739', '1565.3199', '1532.5022',
                        '1844.4434', '1374.6652', '1066.9395', '1277.3526',
                        '1765.7054', '1195.7903', '1403.1857', '1267.8034',
                        '1463.8063', '1567.256', '1986.3291', '1912.5336',
                        '1179.8083', '1539.4475', '1702.7498', '1362.2036',
                        '1605.3957', '1966.5905', '1690.2717', '1796.78',
                        '1965.9646', '1570.6394', '1344.0749', '1505.094',
                        '1500.3763', '1887.334', '1896.9071', '1061.5473',
                        '1210.8434', '1762.6421', '1389.9375', '1747.7094',
                        '1275.7608', '1100.6327', '1832.2851', '1627.4754',
                        '1811.8183', '1202.8991', '1163.3137', '1196.7148',
                        '1318.8771', '1155.3022', '1724.2977', '1737.328',
                        '1289.1381', '1480.495', '1797.7651', '1117.9836',
                        '1108.0792', '1060.2191', '1379.0706', '1513.9224',
                        '1731.9258', '1563.7487', '1988.1656', '1594.7285',
                        '1909.1042', '1920.0818', '1999.9644', '1133.9942',
                        '1608.1459', '1784.159', '1543.759', '1669.3403',
                        '1545.3456', '1177.5607', '1387.8614', '1086.4642',
                        '1514.2136', '1329.4163', '1757.7272', '1574.9939',
                        '1750.1329', '1682.8423', '1331.238', '1330.6685',
                        '1556.6615', '1575.4633', '1754.591', '1456.5672',
                        '1707.2857', '1164.864', '1466.7766', '1383.5692',
                        '1911.8425', '1880.6072', '1278.4999', '1671.8068',
                        '1301.3063', '1071.2867', '1192.7655', '1954.0541',
                        '1041.0466', '1862.7417', '1587.4996', '1242.6044',
                        '1040.399', '1744.3975', '1189.5132', '1885.0033',
                        '1193.7964', '1204.533', '1279.8583', '1488.2298',
                        '1971.1838', '1492.0943', '1722.285', '1947.5481',
                        '1054.343', '1227.5756', '1603.0731', '1948.0095',
                        '1393.6518', '1661.6287', '1829.9104', '1342.3216',
                        '1341.7147', '1994.1765', '1400.0325', '1324.5159',
                        '1355.789', '1538.6368', '1121.0767', '1377.1835',
                        '1831.3158', '1968.0205', '1003.7916', '1502.0367',
                        '1729.5203', '1284.1266', '1252.1786', '1533.2349',
                        '1198.741', '1483.1918', '1528.3996', '1304.2649',
                        '1281.7718', '1441.8902', '1203.4813', '1657.915',
                        '1668.1396', '1560.6021', '1213.1081', '1894.5208',
                        '1791.9156', '1371.9864', '1631.1904', '1635.3301',
                        '1541.2899', '1748.311', '1326.0745', '1736.2491',
                        '1028.1898', '1997.5772', '1764.9201', '1664.4968',
                        '1031.0638', '1457.8448', '1335.8157', '1053.361',
                        '1372.2917', '1847.3652', '1746.7838', '1173.0655',
                        '1653.9771', '1104.8455', '1642.548', '1866.4881',
                        '1381.5643', '1673.6333', '1839.2794', '1855.195',
                        '1698.1673', '1813.0695', '1153.6346', '1354.0321',
                        '1035.5915', '1469.6652', '1422.9333', '1148.4367',
                        '1551.0986', '1047.9434', '1160.0422', '1621.3736']
        self.website = ['twitter', 'twitter', 'twitter', 'twitter', 'twitter',
                        'twitter', 'twitter', 'twitter', 'twitter', 'twitter',
                        'twitter', 'twitter', 'twitter', 'twitter', 'twitter',
                        'twitter', 'twitter', 'twitter', 'twitter', 'twitter',
                        'twitter', 'twitter', 'twitter', 'twitter', 'twitter',
                        'twitter', 'twitter', 'twitter', 'twitter', 'twitter',
                        'twitter', 'twitter', 'twitter', 'twitter', 'twitter',
                        'twitter', 'twitter', 'twitter', 'twitter', 'twitter',
                        'twitter', 'twitter', 'twitter', 'twitter', 'twitter',
                        'twitter', 'twitter', 'twitter', 'twitter', 'twitter',
                        'twitter', 'twitter', 'twitter', 'twitter', 'twitter',
                        'twitter', 'twitter', 'twitter', 'twitter', 'twitter',
                        'twitter', 'twitter', 'twitter', 'twitter', 'twitter',
                        'twitter', 'twitter', 'twitter', 'twitter', 'twitter',
                        'twitter', 'twitter', 'twitter', 'twitter', 'twitter',
                        'twitter', 'twitter', 'twitter', 'twitter', 'twitter',
                        'twitter', 'twitter', 'twitter', 'twitter', 'twitter',
                        'twitter', 'twitter', 'twitter', 'twitter', 'twitter',
                        'twitter', 'twitter', 'twitter', 'twitter', 'twitter',
                        'twitter', 'twitter', 'twitter', 'twitter', 'twitter',
                        'facebook', 'facebook', 'facebook', 'facebook',
                        'facebook', 'facebook', 'facebook', 'facebook',
                        'facebook', 'facebook', 'facebook', 'facebook',
                        'facebook', 'facebook', 'facebook', 'facebook',
                        'facebook', 'facebook', 'facebook', 'facebook',
                        'facebook', 'facebook', 'facebook', 'facebook',
                        'facebook', 'facebook', 'facebook', 'facebook',
                        'facebook', 'facebook', 'facebook', 'facebook',
                        'facebook', 'facebook', 'facebook', 'facebook',
                        'facebook', 'facebook', 'facebook', 'facebook',
                        'facebook', 'facebook', 'facebook', 'facebook',
                        'facebook', 'facebook', 'facebook', 'facebook',
                        'facebook', 'facebook', 'facebook', 'facebook',
                        'facebook', 'facebook', 'facebook', 'facebook',
                        'facebook', 'facebook', 'facebook', 'facebook',
                        'facebook', 'facebook', 'facebook', 'facebook',
                        'facebook', 'facebook', 'facebook', 'facebook',
                        'facebook', 'facebook', 'facebook', 'facebook',
                        'facebook', 'facebook', 'facebook', 'facebook',
                        'facebook', 'facebook', 'facebook', 'facebook',
                        'reddit', 'reddit', 'reddit', 'reddit', 'reddit',
                        'reddit', 'reddit', 'reddit', 'reddit', 'reddit',
                        'reddit', 'reddit', 'reddit', 'reddit', 'reddit',
                        'reddit', 'reddit', 'reddit', 'reddit', 'reddit',
                        'reddit', 'reddit', 'reddit', 'reddit', 'reddit',
                        'reddit', 'reddit', 'reddit', 'reddit', 'reddit',
                        'reddit', 'reddit', 'reddit', 'reddit', 'reddit',
                        'reddit', 'reddit', 'reddit', 'reddit', 'reddit',
                        'reddit', 'reddit', 'reddit', 'reddit', 'reddit',
                        'reddit', 'reddit', 'reddit', 'reddit', 'reddit',
                        'reddit', 'reddit', 'reddit', 'reddit', 'reddit',
                        'reddit', 'reddit', 'reddit', 'reddit', 'reddit',
                        'reddit', 'reddit', 'reddit', 'reddit', 'reddit',
                        'reddit', 'reddit', 'reddit', 'reddit', 'reddit',
                        'reddit', 'reddit', 'reddit', 'reddit', 'reddit',
                        'reddit', 'reddit', 'reddit', 'reddit', 'reddit',
                        'reddit', 'reddit', 'reddit', 'reddit', 'reddit',
                        'reddit', 'reddit', 'reddit', 'reddit', 'reddit',
                        'reddit', 'reddit', 'reddit', 'reddit', 'reddit',
                        'reddit', 'reddit', 'reddit', 'reddit', 'reddit',
                        'reddit', 'reddit', 'reddit', 'reddit', 'reddit',
                        'reddit', 'reddit', 'reddit', 'reddit', 'reddit',
                        'reddit', 'reddit', 'reddit', 'reddit', 'reddit',
                        'reddit', 'reddit', 'reddit', 'reddit', 'reddit']
        self.time = np.array([43.75502506, 32.09982846, 66.44821015,
                              54.67751100, 74.43663107, 64.91509381,
                              101.03624273, 42.50120543, 35.92898678,
                              50.84800153, 46.32394154, 55.82813196,
                              63.90361272, 77.13825762, 78.76436441,
                              53.64704526, 64.75223193, 58.39207272,
                              52.44353642, 60.38707826, 56.51714085,
                              55.72374379, 59.52585080, 62.99625025,
                              40.04902494, 89.02585909, 63.23240605,
                              47.06553888, 73.00190315, 83.80903794,
                              43.41851989, 25.83410322, 68.21623464,
                              50.43442676, 49.98389215, 40.24409163,
                              73.12600309, 59.26529974, 61.66301113,
                              82.24776146, 69.88472085, 55.33333433,
                              40.29625976, 68.09510810, 66.85545440,
                              66.44002527, 72.37790419, 72.81679314,
                              55.09080142, 48.37538346, 47.60326036,
                              51.52223083, 56.51417473, 83.04863572,
                              52.14761947, 81.71073287, 40.88456188,
                              61.76308339, 75.31540245, 64.41482716,
                              52.36763551, 64.48863043, 42.46265519,
                              76.41626766, 73.35103300, 60.13966132,
                              55.09395578, 72.26945197, 64.14173225,
                              59.39558958, 54.92166432, 56.15937888,
                              35.82839971, 80.22338349, 52.03277136,
                              30.46794613, 58.48158453, 51.08064303,
                              67.56882508, 64.67001088, 70.31701029,
                              69.69418892, 45.40860831, 68.72559847,
                              57.18659048, 79.66512776, 54.12521925,
                              81.23543425, 79.58214820, 34.09101162,
                              34.07926981, 53.68661297, 84.73351889,
                              76.98667389, 83.91038109, 66.35125602,
                              43.38243470, 60.07458569, 64.01561208,
                              70.66573983, 193.40761370, 149.46771172,
                              178.54940784, 146.81737462, 112.67080963,
                              105.79566831, 169.60015351, 18.16782312,
                              32.33793705, 161.72043630, 136.65935083,
                              23.99200240, 124.30215961, 82.66230873,
                              181.53122374, 96.73843934, 149.75297762,
                              119.92104479, 29.30535556, 88.98066487,
                              82.18281694, 99.76251178, 120.62310261,
                              136.15837651, 140.85019656, 117.06990731,
                              163.65366512, 214.50717765, 79.72206954,
                              138.03112015, 144.45114437, 16.41512219,
                              72.08551518, 85.46372630, 149.13372767,
                              76.92212059, 109.55645713, 141.65595764,
                              119.18734692, 51.20662038, 183.75411201,
                              132.56555213, 101.55378472, 177.69500317,
                              130.27160521, 143.13166882, 107.23696643,
                              212.72330518, 130.66925461, 210.11532010,
                              118.65653641, 77.25638890, 153.29389237,
                              146.97514023, 0, 105.83704268,
                              200.05768527, 166.46158871, 135.60586892,
                              111.06739555, 71.50642636, 21.58216051,
                              183.15691697, 38.58822892, 38.84706613,
                              119.36492288, 108.77038019, 88.70541115,
                              12.61048676, 0, 157.77516036,
                              43.70631550, 193.87291179, 203.26411137,
                              179.20054809, 148.37792309, 170.38620220,
                              102.23651707, 63.46142967, 82.33043919,
                              258.68968847, 223.94730803, 281.46276889,
                              350.40078080, 281.53639290, 305.90987647,
                              286.22932832, 356.53308940, 276.81798226,
                              305.04298118, 299.13866751, 310.41638501,
                              347.77589112, 278.37912458, 295.00398672,
                              292.23076451, 348.14209652, 289.14551826,
                              288.86118512, 299.21300848, 264.29449774,
                              353.26294987, 275.68453639, 279.45885854,
                              287.79470948, 303.34990705, 324.73398364,
                              337.50702196, 326.59649321, 307.14724645,
                              300.13203731, 335.28447725, 273.59560986,
                              315.71949943, 268.86100671, 309.44822617,
                              357.67123883, 313.70684577, 311.99209985,
                              277.87145259, 316.89239037, 254.39694340,
                              300.02140552, 237.21539997, 329.92714491,
                              318.32432005, 326.65600788, 305.40145477,
                              326.78894825, 318.92641904, 320.59443395,
                              308.26919092, 300.00328438, 294.61849344,
                              284.55947774, 277.63798594, 359.44015820,
                              292.55982554, 322.71946292, 318.60262991,
                              307.93128984, 282.51266904, 304.74114309,
                              285.30356994, 240.53264849, 252.69086070,
                              289.49431273, 284.68590654, 317.95577632,
                              288.39433522, 303.55186227, 286.21794163,
                              281.11550530, 297.15770465, 307.37441274,
                              290.21885096, 297.39693356, 325.12591032,
                              340.14615302, 314.10755364, 321.41818630,
                              302.46825284, 272.60859596, 285.02155314,
                              260.57728373, 301.01186081, 314.01532677,
                              301.39435122, 301.53108663, 290.81233377,
                              331.20632569, 329.26192444, 252.12513671,
                              294.17604509, 314.25160994, 260.22225619,
                              296.06068483, 328.70473699, 293.72532762,
                              323.92449714, 279.36077985, 327.10547840,
                              332.33552711, 244.70073987, 368.94370441,
                              288.52914183, 270.96734651, 321.09234466,
                              395.74872017, 311.64415600, 314.81990465,
                              319.70690366, 313.96061624, 275.38526052,
                              338.02460670, 286.98781666, 353.55909038,
                              306.62353307, 306.92733543, 273.74222557])

        # # Creates a data frame object
        self.df = DataFrame({'WEBSITE': Series(self.website, index=self.ids),
                             'DWELL_TIME': Series(self.time, index=self.ids)})

        # Creates the distance matrix object
        self.ids2 = np.array(['000001181.5654', '000001096.8485',
                              '000001348.2238', '000001239.2471',
                              '000001925.5603', '000001148.4367',
                              '000001551.0986', '000001047.9434',
                              '000001160.0422', '000001621.3736'])
        self.map = self.df.loc[self.ids2]
        dist = np.array([[0.000, 0.297, 0.257, 0.405, 0.131, 0.624, 0.934,
                          0.893, 0.519, 0.904],
                         [0.297, 0.000, 0.139, 0.130, 0.348, 1.000, 0.796,
                          1.000, 0.647, 0.756],
                         [0.257, 0.139, 0.000, 0.384, 0.057, 0.748, 0.599,
                          0.710, 0.528, 1.000],
                         [0.405, 0.130, 0.384, 0.000, 0.303, 0.851, 0.570,
                          0.698, 1.000, 0.638],
                         [0.131, 0.348, 0.057, 0.303, 0.000, 0.908, 1.000,
                          0.626, 0.891, 1.000],
                         [0.624, 1.000, 0.748, 0.851, 0.908, 0.000, 0.264,
                          0.379, 0.247, 0.385],
                         [0.934, 0.796, 0.599, 0.570, 1.000, 0.264, 0.000,
                          0.336, 0.326, 0.530],
                         [0.893, 1.000, 0.710, 0.698, 0.626, 0.379, 0.336,
                          0.000, 0.257, 0.450],
                         [0.519, 0.647, 0.528, 1.000, 0.891, 0.247, 0.326,
                          0.257, 0.000, 0.492],
                         [0.904, 0.756, 1.000, 0.638, 1.000, 0.385, 0.530,
                          0.450, 0.492, 0.000]])
        self.dm = skbio.DistanceMatrix(dist, self.ids2)
        self.taxa = ['k__Bacteria; p__[Proteobacteria]; '
                     'c__Gammaproteobacteria; o__; f__; g__; s__',
                     'k__Bacteria; p__Proteobacteria; '
                     'c__Gammaproteobacteria; o__Enterobacteriales; '
                     'f__Enterbacteriaceae; g__Escherichia; s__coli']

        self.sub_p = DataFrame(np.array([['ref_group1 vs. ref_group1', 
                                          'ref_group1 vs. group1', 0.01],
                                         ['ref_group2 vs. group2', 
                                          'ref_group2 vs. ref_group2', 0.02],
                                         ['group3 vs. ref_group3', 
                                          'ref_group3 vs. ref_group3', 0.03],
                                         ['ref_group4 vs. ref_group4',
                                          'group4 vs. ref_group4', 0.04]]),
                               columns=['Group 1', 'Group 2', 'p_value'])
        self.sub_p.p_value = self.sub_p.p_value.astype(float)
        self.sub_p_lookup = {k: set(self.sub_p[k].values) for k in 
                             ('Group 1', 'Group 2')}

    def test_pad_index_default(self):
        # Creates a data frame with raw ids and no sample column
        df = DataFrame({'#SampleID': self.raw_ids,
                        'WEBSITE': Series(self.website),
                        'DWELL_TIME': Series(self.time)})
        # Pads the raw text
        df = pad_index(df)
        assert_index_equal(self.df.index, df.index)

    def test_pad_index_custom_index(self):
        # Creates a data frame with raw ids and no sample column
        df = DataFrame({'RawID': self.raw_ids,
                        'WEBSITE': Series(self.website),
                        'DWELL_TIME': Series(self.time)})
        # Pads the raw text
        df = pad_index(df, index_col='RawID')
        assert_index_equal(self.df.index, df.index)

    def test_pad_index_number(self):
        # Creates a data frame with raw ids and no sample column
        df = DataFrame({'#SampleID': self.raw_ids,
                        'WEBSITE': Series(self.website),
                        'DWELL_TIME': Series(self.time)})
        # Pads the raw text
        df = pad_index(df, nzeros=4)
        assert_index_equal(Index(self.raw_ids), df.index)

    def test_check_dir(self):
        # Sets up a dummy directory that does not exist
        does_not_exist = pjoin(TEST_DIR, 'this_dir_does_not_exist')
        # Checks the directory does not currently exist
        self.assertFalse(exists(does_not_exist))
        # checks the directory
        check_dir(does_not_exist)
        # Checks the directory exists now
        self.assertTrue(exists(does_not_exist))
        # Removes the directory
        rmdir(does_not_exist)

    def test_post_hoc_pandas(self):
        known_index = Index(['twitter', 'facebook', 'reddit'],
                            name='WEBSITE')
        known_df = DataFrame(np.array([[100,  60.435757,  60.107124, 14.632637,
                                        np.nan, np.nan],
                                       [80, 116.671135, 119.642984, 54.642403,
                                        7.010498e-14, np.nan],
                                       [120, 302.615690, 301.999670,
                                        28.747101, 2.636073e-37,
                                        5.095701e-33]]),
                             index=known_index,
                             columns=['Counts', 'Mean', 'Median', 'Stdv',
                                      'twitter', 'facebook'])
        known_df.Counts = known_df.Counts.astype('int64')
        test_df = post_hoc_pandas(self.df, 'WEBSITE', 'DWELL_TIME')
        assert_frame_equal(known_df, test_df)

    def test_multiple_correct_post_hoc(self):
        known_df = DataFrame(np.array([[np.nan, 4e-2, 1e-3],
                                       [4e-4, np.nan, 1e-6],
                                       [4e-7, 4e-8, np.nan]]),
                             columns=[0, 1, 2])
        raw_ph = DataFrame(np.power(10, -np.array([[np.nan, 2, 3],
                                                   [4, np.nan, 6],
                                                   [7, 8, np.nan]])),
                           columns=[0, 1, 2])
        order = np.arange(0, 3)
        test_df = multiple_correct_post_hoc(raw_ph, order, 'fdr_bh')
        assert_frame_equal(known_df, test_df)

    def test_segemented_colormap(self):
        known_cmap = np.array([[0.88207613, 0.95386390, 0.69785469,  1.],
                               [0.59215687, 0.84052289, 0.72418302,  1.],
                               [0.25268744, 0.71144946, 0.76838141,  1.],
                               [0.12026144, 0.50196080, 0.72156864,  1.],
                               [0.14136102, 0.25623991, 0.60530568,  1.]])
        test_cmap = segment_colormap('YlGnBu', 5)
        npt.assert_almost_equal(test_cmap, known_cmap, 5)

    def test_get_bar_height(self):
        test_lowest, test_fudge = \
            _get_bar_height(np.array([0.01, 0.02, 0.3, 0.52]))
        npt.assert_almost_equal(test_lowest, 0.55, 3)
        self.assertEqual(test_fudge, 10)

    def test_get_bar_height_fudge(self):
        test_lowest, test_fudge = \
            _get_bar_height(np.array([0.01, 0.02, 0.3, 0.52]), factor=3)
        self.assertEqual(test_lowest, 0.54)
        self.assertEqual(test_fudge, 10)

    def test_get_p_value(self):
        self.assertEqual(_get_p_value(self.sub_p, self.sub_p_lookup, 
                                      'ref_group1', 'group1', 'p_value'), 0.01)
        self.assertEqual(_get_p_value(self.sub_p, self.sub_p_lookup,
                                      'ref_group2', 'group2', 'p_value'), 0.02)
        self.assertEqual(_get_p_value(self.sub_p, self.sub_p_lookup,
                                      'ref_group3', 'group3', 'p_value'), 0.03)
        self.assertEqual(_get_p_value(self.sub_p, self.sub_p_lookup,
                                      'ref_group4', 'group4', 'p_value'), 0.04)

    def test_get_p_value_error(self):
        with self.assertRaises(ValueError):
            _get_p_value(self.sub_p, self.sub_p_lookup, 'ref_group',
                         'group', 'p_value')

    def test_correct_p_value_no_tail(self):
        p_value = 0.05
        tail = False
        self.assertEqual(_correct_p_value(tail, p_value, 1, 1), p_value)

    def test_correct_p_value_no_greater_ref(self):
        p_value = 0.05
        tail = True
        self.assertEqual(_correct_p_value(tail, p_value, 2, 1), 1)

    def test_correct_p_value_no_less_ref(self):
        p_value = 0.05
        tail = True
        self.assertEqual(_correct_p_value(tail, p_value, 1, 2), p_value)

    def test_get_distance_vectors(self):
        known_within = {'twitter': np.array([0.297, 0.257, 0.405, 0.131, 
                                             0.139, 0.130, 0.348, 0.384,
                                              0.057, 0.303]),
                        'reddit': np.array([0.264, 0.379, 0.247, 0.385, 0.336,
                                            0.326, 0.530, 0.257, 0.450, 
                                            0.492])}
        known_between = {('twitter', 'reddit'): np.array([0.624, 0.934, 0.893,
                                                          0.519, 0.904, 1.000,
                                                          0.796, 1.000, 0.647,
                                                          0.756, 0.748, 0.599,
                                                          0.710, 0.528, 1.000,
                                                          0.851, 0.570, 0.698,
                                                          1.000, 0.638, 0.908,
                                                          1.000, 0.626, 0.891,
                                                          1.000])} 
        test_within, test_between = \
            get_distance_vectors(dm=self.dm,
                                 df=self.map,
                                 group='WEBSITE',
                                 order=['twitter', 'reddit'])
        # Tests the results
        self.assertEqual(known_within.keys(), test_within.keys())
        self.assertEqual(known_between.keys(), test_between.keys())
        for k, a in test_within.iteritems():
            npt.assert_array_equal(known_within[k], a)
        for k, a in test_between.iteritems():
            npt.assert_array_equal(known_between[k], a)

    def test_split_taxa_error(self):
        with self.assertRaises(ValueError):
            split_taxa(['k__Bacteria; p__[Proteobacteria]; '
                        'c__Gammaproteobacteria'], 7)

    def test_split_taxa(self):
        known_taxa = np.array([['Bacteria', 'cont. Proteobacteria',
                                'Gammaproteobacteria',
                                'c. Gammaproteobacteria',
                                'c. Gammaproteobacteria',
                                'c. Gammaproteobacteria',
                                'c. Gammaproteobacteria'],
                               ['Bacteria', 'Proteobacteria',
                                'Gammaproteobacteria', 'Enterobacteriales',
                                'Enterbacteriaceae', 'Escherichia', 'coli']],
                              dtype='|S32')
        known_levels = ['kingdom', 'phylum', 'p_class', 'p_order', 'family',
                        'genus', 'species']
        test_taxa, test_levels = split_taxa(self.taxa, 7)
        self.assertEqual(known_levels, test_levels)
        npt.assert_array_equal(known_taxa, test_taxa)

    def test_get_ratio_heatmap(self):
        data = np.array([[1, 2,  3,   4],
                         [2, 4,  6,   8],
                         [3, 6,  9,  12],
                         [4, 8, 12, 16]])
        known = np.array([[0.4, 0.8, 1.2, 1.6],
                          [0.4, 0.8, 1.2, 1.6],
                          [0.4, 0.8, 1.2, 1.6],
                          [0.4, 0.8, 1.2, 1.6]])
        test = get_ratio_heatmap(data)
        npt.assert_array_equal(test, known)

    def test_get_ratio_heatmap_log(self):
        data = np.array([[2, 4,  8,  16],
                         [1, 4, 16, 256]])
        known = np.array([[0, 1, 2, 3],
                          [0, 2, 4, 8]])
        test = get_ratio_heatmap(data, ref_pos=0, log=2)
        npt.assert_array_equal(test, known)


if __name__ == '__main__':
    main()
