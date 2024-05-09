# Preface

This book introduces the reader to the world of machine learning on graphs. It is a project-based book, where the reader learns by doing. In each part, we will introduce a new concept, learn the theory behind it, and then apply it to a real-world problem.

# Introduction to the Book

## Machine Learning in the Connected World

### What's the fuss

Our world without interactions would be a dull universe of elementary particles that float around. Interactions are what make our universe interesting. Interactions between the elementary particles make the atoms, interactions between atoms make molecules, interactions between molecules make materials... you get the idea. Moreover, interactions between people make communities, and interactions between computers make the Internet.

If we want to study these interactions using computational tools, we need a way to represent them and deal with them. The mathematical structure that is most suitable for this exploration has the unfortunate fate to have a pretty misleading name - *graphs*. Sometimes, these graphs are called *networks*. The terms that deal with graph components are also sometimes misleading and confusing: we talk about nodes and edges, paths and components, but their meaning in our context will be slightly different from what you are used to in the English language.

For example, in the year 1967, Stanley Milgram and his colleagues conducted a famous experiment demonstrating that human society behaves like a very small world, where it is usually enough to have six introductions in order to connect two randomly picked people (Milgram, S. (1967). *The small world problem*. Psychology Today, 2(1), 60-67). This phenomenon, known as the six degrees of separation, highlights the interconnectedness of our world through social networks.

More recently, Lada Adamic analyzed cross-links between political blogs and discovered strong communities with distinct liberal and conservative leanings (Adamic, L. A., & Glance, N. S. (2005). *The political blogosphere and the 2004 U.S. election: Divided they blog*. Proceedings of the WWW-2005 Workshop on the Weblogging Ecosystem, 36-43). If you look at the central figure from Adamic's paper, you'll see each blog represented by a dot (we call them nodes) and a connection between two nodes representing cross-links between the blogs (we call them edges). You will notice how strikingly strong the separation between liberal and conservative blogs is. Keep in mind that this separation of the dots in that figure is not a result of the research team marking each blog, but rather a result of a relatively simple mathematical analysis, which you will learn in the course of this book.

In another research, Dr. Adamic studied millions of recipes online. Again, she used machine learning to automatically identify communities of recipes based on ingredient similarity (REF Teng, C.-Y., Lin, Y.-R., & Adamic, L. A. (2021). Recipe recommendation using ingredient networks.).

Another prominent scientist, Albert-Laszlo Barabási, used network science to explore the "rich-get-richer" phenomenon. His work shows that many real-world networks, like the web or social networks, follow a pattern where a small number of nodes have a very high number of connections, while the vast majority have only a few connections. In the context of social networks, for example, this translates to a situation where a few popular individuals accumulate a large number of followers, while most users have a smaller number of connections (Measuring preferential attachment for evolving networks
H. Jeong, Z. N ́eda∗ and A.L. Baraba ́si).

Jure Leskovec is yet another prominent network scientist. In 2007, he and his colleagues showed that the structure of the network can be used to predict future connections in the network (Leskovec, J., Kleinberg, J., & Faloutsos, C. (2007). *Graph evolution: Densification and shrinking diameters*. ACM Transactions on Knowledge Discovery from Data (TKDD), 1(1), 2).

In my practice as a freelance data scientist (if I may add myself to the list of these prominent scientists), I have analyzed the collaboration patterns of managers of daughter companies of a large multinational corporation. Once I built the network of collaborations, we could immediately see how three large groups of managers emerged. These groups were not a result of the company's organizational structure, but rather a result of the collaboration patterns of the managers. Having identified these groups, I could measure the strength of the connections between them, suggest ways to improve the collaboration, and select the most suitable managers for spreading the best practices across the company.

Earlier in my career, I used graph algorithms to identify fraudulent banking transactions. By analyzing networks of transactions and cardholders, algorithms can detect suspicious patterns.

Come with me on a journey to the world of graphs and networks. We will learn how to represent and analyze interactions between people, computers, and molecules. We will learn how to identify key influencers in social networks, detect communities in social media, model the spread of information, and detect fraud in financial networks. We will learn how to apply these techniques to real-world problems and make a difference in the world.

# Chapter 1: Connecting the Dots

**Introduction to Graphs and Graph Algorithms**

The first part, "Connecting the Dots," introduces the reader to the world of graphs and graph algorithms. We'll learn what graphs are, basic terms and definitions, and how to work with graphs in Python. At the end of the part, we'll explore the fascinating concept of the "small world phenomenon."

Key concepts: graphs, nodes, edges, adjacency matrix, adjacency list, breadth-first search, depth-first search, shortest path.
