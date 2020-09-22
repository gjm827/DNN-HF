# Hybrid Microblog Recommendation with Heterogeneous Features Using Deep Neural Network
## Introduction
With the development of mobile Internet, microblog has become one of the most popular social platforms. The enormous user-generated microblogs have caused the problem of information overload, which makes users difficult to find the microblogs they actually need. Hence, how to provide users with accurate microblogs has become a hot and urgent issue. In this paper, we propose an approach of hybrid microblog recommendation, which is developed on a framework of deep neural network with a group of heterogeneous features as its input. Specifically, two new recommendation strategies are first constructed in terms of the extended user-interest tags and user interest topics, respectively. These two strategies additionally with the collaborative filtering are employed together to obtain the candidate microblogs for final recommendation. Then, we propose the heterogeneous features related to personal interests of users, interest in authors and microblog quality to describe the candidate microblogs. Finally, a deep neural network with multiple hidden layers is designed to predict and rank the microblogs. Extensive experiments conducted on the datasets of Sina Weibo and Twitter indicate that the proposed approach significantly outperforms the state-of-the-art methods. 

## Implementation
### 1. The three microblog recommendation strategies
#### 1.1 Microblog recommendation based on the extended user interest tags (EUIT)
Path: \DNN-HF\Recall\RecommendationBasedonEUIT

* compute_word_weight_by_TFIDF.py: compute keywords' weights by TF-IDF.

* get_user_tag_by_EUIT.py: calculate keywords' weights by TextRank with TF-IDF, and then use association rules to extend them, obtaining extended user interest tags.

* recommendation_based_on_EUIT.py: conduct recommendation based on extended user interest tags, generating the set A of candidate recommended microblogs.

#### 1.2 Microblog recommendation based on user interest topics (UT)
Path: \DNN-HF\Recall
* recommendation_based_on_UT.py: compute topic weight by TF-IDF, and then conduct recommendation based on user interest topics, generating the set B of candidate recommended microblogs.

#### 1.3  Microblog recommendation using user-based collaborative filtering (CF)
Path: \DNN-HF\Recall
* recommendation_based_on_CF.py: compute user similarity by four methods: user content, interactive behaviors, and two methods based on social relationship. Then recommend microblogs based on interactive behavior similarity, generating the set C of candidate recommended microblogs.

### 2. Microblog sorting
Path: \DNN-HF\Sort
* get_feature.py: generate eight heterogeneous features for each microblog.

* model.py: the deep neural network for microblog sorting, generating the set Mr of recommended microblogs.

## Baselines
### 1. Mining microblog user interests based on TextRank with TF-IDF factor (TTI) [1]
Path: \Baselines\TTI

* compute_word_weight_by_TFIDF.py: compute keywords' weights by TF-IDF.

* get_user_tag_by_TTI.py: calculate keywords' weights by TextRank with TF-IDF and generate user tags.

* recommendation_based_on_TTI.py: recommend microblogs based on user tags.

### 2. A microblog recommendation algorithm based on multi-tag correlation (TC) [2]

Path: \Baselines\TC

* user_tag_retrieval.py: compute keywords' weight by TF-IDF and TF-Clarity, and generate user tags.

* multi-tags_correlation.py：calculate multi-tags inner correlation and outer correlation.

* update_user-tag_matrix.py: update the user-tag matrix by tag inner and outer correlation.

* recommend_based_on_TC.py: compute the similarity between microblogs and users, and generate recommended microblogs.

### 3. Combining tag correlation and user social relation for microblog recommendation (ITCAUSR) [3]

Path: \Baselines\ITCAUSR

* user_tag_retrieval.py: compute keywords' weight by TF-IDF and TF-Clarity, and generate user tags.

* multi-tags_correlation.py：calcuate multi-tags inner correlation and outer correlation.

* update_user-tag_matrix.py: update the user-tag matrix by tag inner and outer correlation.

* social_relation.py: generate user-user social relation similarity matrix.

* matrix_iteration.py: conduct matrix iteration to obtain the final user-tag matrix.

* recommend_based_on_ITCAUSR.py: calculate the similarity between microblogs and users, and generate recommended microblogs.

##References

[1] Tu, S., and Huang, M. (2016). Mining microblog user interests based on textrank with tf-idf factor. The Journal of China Universities of Posts and Telecommunications, 23(5):40–46.

[2] Ma, H., Jia, M., Xie, M., and Lin, X. (2015). A microblog recommendation algorithm based on multi-tag correlation. In International Conference on Knowledge Science, Engineering and Management, pages 483–488. Springer.

[3] Ma, H., Jia, M., Zhang, D., and Lin, X. (2017). Combining tag correlation and user social relation for microblog recommendation. Information Sciences, 385:325–337.
