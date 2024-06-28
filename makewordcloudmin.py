#!venv/bin/python

import collections
import matplotlib.pyplot as plt
import wordcloud

if __name__ == "__main__":

    text = " ".join(["sme"] * 10 + ["r&d"] * 10)

    frequencies = collections.Counter()
    for word in text.split(" "):
        frequencies[word] += 1
    frequencies = dict(frequencies)

    cloud = wordcloud.WordCloud().generate(text)
    plt.imshow(cloud)
    plt.tight_layout(pad=0)
    plt.axis('off')
    plt.title('text')
    plt.show(bbox_inches='tight')

    cloud = wordcloud.WordCloud().generate_from_frequencies(frequencies)
    plt.imshow(cloud)
    plt.tight_layout(pad=0)
    plt.axis('off')
    plt.title('frequencies')
    plt.show(bbox_inches='tight')
