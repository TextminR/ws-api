from elasticsearch import Elasticsearch

es = Elasticsearch(
    ['http://localhost:9200'],
    basic_auth=("elastic", "GZLhtJXfckU-DcYQLgYU"),
    verify_certs=False
)

authors =[
  {
    "name": "Stoker, Bram",
    "birth_place": "Dublin, Ireland",
    "lat": "53.3498",
    "long": "-6.2603",
    "country": "IE"
  },
  {
    "name": "Wilde, Oscar",
    "birth_place": "Dublin, Ireland",
    "lat": "53.3498",
    "long": "-6.2603",
    "country": "IE"
  },
  {
    "name": "Fitzgerald, F. Scott (Francis Scott)",
    "birth_place": "Saint Paul, Minnesota, United States",
    "lat": "44.9537",
    "long": "-93.0900",
    "country": "US"
  },
  {
    "name": "Ibsen, Henrik",
    "birth_place": "Skien, Norway",
    "lat": "59.2089",
    "long": "9.6090",
    "country": "NO"
  },
  {
    "name": "Salten, Felix",
    "birth_place": "Pest, Hungary",
    "lat": "47.4979",
    "long": "19.0402",
    "country": "HU"
  },
  {
    "name": "Gilman, Charlotte Perkins",
    "birth_place": "Hartford, Connecticut, United States",
    "lat": "41.7637",
    "long": "-72.6851",
    "country": "US"
  },
  {
    "name": "Doyle, Arthur Conan",
    "birth_place": "Edinburgh, Scotland",
    "lat": "55.9533",
    "long": "-3.1883",
    "country": "GB"
  },
  {
    "name": "Twain, Mark",
    "birth_place": "Florida, Missouri, United States",
    "lat": "39.4808",
    "long": "-91.7938",
    "country": "US"
  },
  {
    "name": "Du Bois, W. E. B. (William Edward Burghardt)",
    "birth_place": "Great Barrington, Massachusetts, United States",
    "lat": "42.1959",
    "long": "-73.3621",
    "country": "US"
  },
  {
    "name": "Tolstoy, Leo, graf",
    "birth_place": "Yasnaya Polyana, Tula, Russia",
    "lat": "54.0813",
    "long": "37.5253",
    "country": "RU"
  },
  {
    "name": "Conrad, Joseph",
    "birth_place": "Berdychiv, Ukraine",
    "lat": "49.8950",
    "long": "28.5997",
    "country": "UA"
  },
  {
    "name": "Joyce, James",
    "birth_place": "Dublin, Ireland",
    "lat": "53.3498",
    "long": "-6.2603",
    "country": "IE"
  },
  {
    "name": "Barrie, J. M. (James Matthew)",
    "birth_place": "Kirriemuir, Angus, Scotland",
    "lat": "56.6739",
    "long": "-2.9916",
    "country": "GB"
  },
  {
    "name": "Baum, L. Frank (Lyman Frank)",
    "birth_place": "Chittenango, New York, United States",
    "lat": "43.0451",
    "long": "-75.8668",
    "country": "US"
  },
  {
    "name": "Montgomery, L. M. (Lucy Maud)",
    "birth_place": "New London, Prince Edward Island, Canada",
    "lat": "46.4635",
    "long": "-63.5167",
    "country": "CA"
  },
  {
    "name": "Leblanc, Maurice",
    "birth_place": "Rouen, France",
    "lat": "49.4432",
    "long": "1.0999",
    "country": "FR"
  },
  {
    "name": "Nietzsche, Friedrich Wilhelm",
    "birth_place": "Röcken bei Lützen, Germany",
    "lat": "51.2502",
    "long": "12.1607",
    "country": "DE"
  },
  {
    "name": "Milne, A. A. (Alan Alexander)",
    "birth_place": "Kilburn, London, United Kingdom",
    "lat": "51.5465",
    "long": "-0.1909",
    "country": "GB"
  },
  {
    "name": "Gibran, Kahlil",
    "birth_place": "Bsharri, Lebanon",
    "lat": "34.2333",
    "long": "36.0000",
    "country": "LB"
  },
  {
    "name": "Herzl, Theodor",
    "birth_place": "Budapest, Hungary",
    "lat": "47.4979",
    "long": "19.0402",
    "country": "HU"
  },
  {
    "name": "Wells, H. G. (Herbert George)",
    "birth_place": "Bromley, Kent, England",
    "lat": "51.4060",
    "long": "0.0132",
    "country": "GB"
  },
  {
    "name": "Thompson, D'Arcy Wentworth",
    "birth_place": "Edinburgh, Scotland",
    "lat": "55.9533",
    "long": "-3.1883",
    "country": "GB"
  },
  {
    "name": "Chambers, Robert W. (Robert William)",
    "birth_place": "Brooklyn, New York, United States",
    "lat": "40.6782",
    "long": "-73.9442",
    "country": "US"
  },
  {
    "name": "Russell, Bertrand",
    "birth_place": "Trellech, Monmouthshire, United Kingdom",
    "lat": "51.7250",
    "long": "-2.7170",
    "country": "GB"
  },
  {
    "name": "Shelley, Mary Wollstonecraft",
    "birth_place": "London, United Kingdom",
    "lat": "51.5074",
    "long": "-0.1278",
    "country": "GB"
  },
  {
    "name": "Shakespeare, William",
    "birth_place": "Stratford-upon-Avon, Warwickshire, England",
    "lat": "52.1917",
    "long": "-1.7073",
    "country": "GB"
  },
  {
    "name": "Austen, Jane",
    "birth_place": "Steventon, Hampshire, England",
    "lat": "51.2681",
    "long": "-1.0923",
    "country": "GB"
  },
  {
    "name": "Hawthorne, Nathaniel",
    "birth_place": "Salem, Massachusetts, United States",
    "lat": "42.5195",
    "long": "-70.8967",
    "country": "US"
  },
  {
    "name": "Carroll, Lewis",
    "birth_place": "Daresbury, Cheshire, England",
    "lat": "53.3420",
    "long": "-2.6035",
    "country": "GB"
  },
  {
    "name": "Swift, Jonathan",
    "birth_place": "Dublin, Ireland",
    "lat": "53.3498",
    "long": "-6.2603",
    "country": "IE"
  },
  {
    "name": "Stevenson, Robert Louis",
    "birth_place": "Edinburgh, Scotland",
    "lat": "55.9533",
    "long": "-3.1883",
    "country": "GB"
  },
  {
    "name": "Dickens, Charles",
    "birth_place": "Portsmouth, Hampshire, England",
    "lat": "50.8198",
    "long": "-1.0886",
    "country": "GB"
  },
  {
    "name": "Irving, Washington",
    "birth_place": "New York City, New York, United States",
    "lat": "40.7128",
    "long": "-74.0060",
    "country": "US"
  },
  {
    "name": "Melville, Herman",
    "birth_place": "New York City, New York, United States",
    "lat": "40.7128",
    "long": "-74.0060",
    "country": "US"
  },
  {
    "name": "Brontë, Charlotte",
    "birth_place": "Thornton, West Yorkshire, England",
    "lat": "53.7950",
    "long": "-1.8640",
    "country": "GB"
  },
  {
    "name": "Machiavelli, Niccolò",
    "birth_place": "Florence, Italy",
    "lat": "43.7696",
    "long": "11.2558",
    "country": "IT"
  },
  {
    "name": "Homer",
    "birth_place": "Ionia, Ancient Greece",
    "lat": "38.4314",
    "long": "27.1390",
    "country": "GR"
  },
  {
    "name": "United States. Office of Strategic Services",
    "birth_place": "United States",
    "lat": "38.9072",
    "long": "-77.0369",
    "country": "US"
  }
]

for doc in authors:
    es.index(index="authors", document=doc)