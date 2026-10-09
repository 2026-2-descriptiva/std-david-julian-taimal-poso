from .s01_ingest import s01_ingest
from .s02_make_documents_by_year_plot import s02_make_documents_by_year_plot
from .s03_countries_create import s03_countries_create
from .s04_countries_clean import s04_countries_clean
from .s05_countries_frequency_report import s05_countries_frequency_report
from .s06_countries_frequency_plot import s06_countries_frequency_plot
from .s07_countries_world_map import s07_countries_world_map
from .s08_countries_cooc_matrix import s08_countries_cooc_matrix
from .s09_countries_heatmap import s09_countries_heatmap
from .s10_countries_clusters import s10_countries_clusters
from .s11_countries_network import s11_countries_network
from .s12_sources_frequency_report import s12_sources_frequency_report
from .s13_authors_frequency_report import s13_authors_frequency_report
from .s14_keywords_create import s14_keywords_create
from .s15_keywords_clean import s15_keywords_clean
from .s16_keywords_frequency_report import s16_keywords_frequency_report
from .s17_keywords_cooc_matrix import s17_keywords_cooc_matrix
from .s18_keywords_filter import s18_keywords_filter
from .s19_keywords_clusters import s19_keywords_clusters
from .s20_keywords_network import s20_keywords_network


def main():
    s01_ingest()
    s02_make_documents_by_year_plot()
    s03_countries_create()
    s04_countries_clean()
    s05_countries_frequency_report()
    s06_countries_frequency_plot()
    s07_countries_world_map()
    s08_countries_cooc_matrix()
    s09_countries_heatmap()
    s10_countries_clusters()
    s11_countries_network()
    s12_sources_frequency_report()
    s13_authors_frequency_report()
    s14_keywords_create()
    s15_keywords_clean()
    s16_keywords_frequency_report()
    s17_keywords_cooc_matrix()
    s18_keywords_filter()
    s19_keywords_clusters()
    s20_keywords_network()


if __name__ == "__main__":
    main()