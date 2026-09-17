# Random species generator

Someone I know wanted a random species generator but was frustrated by the amount of beetles for a true random generator. This one lets you filter by class (e.g. Mammalia). It then searches on wikidata to get other names.

It uses the dataset from the [catalogue of life](https://www.gbif.org/dataset/7ddf754f-d193-4cc9-b351-99906754a03b). I unzipped, picked out Taxon.tsv, imported into pandas and put into an sqlite db.

```python
import pandas as pd
import csv
from sqlalchemy import create_engine

df = pd.read_csv('data/Taxon.tsv',sep = '\t', quoting=csv.QUOTE_NONE)
engine = create_engine('sqlite:///species.db', echo=False)

df.to_sql(name='taxons', con=engine)
```

I've created indices on `dwc:kingdom`, `dwc:phylum`, and `dwc:class`.

It uses the wikidata sdk. into `static`:
```bash
wget https://raw.githubusercontent.com/maxlath/wikibase-sdk/v8.1.1/dist/wikibase-sdk.min.js
wget https://raw.githubusercontent.com/maxlath/wikibase-sdk/v8.1.1/dist/wikidata-sdk.min.js
```


