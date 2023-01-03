# Setup

## Install web scraper dependencies

1. Install dependencies

```
npm ci
```

2. Rename `.env.sample` to `.env` and update accordingly.

## Install embedding generator dependencies

1. Install virtualenv

```
pip3 install virtualenv
```

2. Create virtual environment

```
virtualenv venv
```

3. Activate the virtual environment

```
source venv/bin/activate
```

4. Install dependencies

```
pip3 install -r requirements.txt
```

# Generating service bundles embeddings

1. Run scraper. This scrapes all service bundles that are currently published. Output will be in `data/scraper-results.json`.

```
npm run scrape
```

2. Run embedding generator. Output will be in `data/embeddings.json`. This json should be copied into mol-personalise scripts to generate the payload.

```
npm run embedding:generate
```
