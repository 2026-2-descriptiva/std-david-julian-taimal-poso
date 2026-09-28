from pathlib import Path


def test_01():
    assert Path("submission/authors_frequency.csv").is_file()
    assert Path("submission/country_clusters.txt").is_file()
    assert Path("submission/country_collab_network.html").is_file()
    assert Path("submission/country_cooc_heatmap.html").is_file()
    assert Path("submission/country_cooc_matrix.csv").is_file()
    assert Path("submission/country_frequency.csv").is_file()
    assert Path("submission/country_frequency_plot.html").is_file()
    assert Path("submission/documents_by_year.html").is_file()
    assert Path("submission/keywords_clusters.txt").is_file()
    assert Path("submission/keywords_cooc_matrix.csv").is_file()
    assert Path("submission/keywords_cooc_network.html").is_file()
    assert Path("submission/keywords_frequency.csv").is_file()
    assert Path("submission/scopus.csv.gz").is_file()
    assert Path("submission/source_frequency.csv").is_file()
    assert Path("submission/world_map.html").is_file()
