# Budget

Budget is an open source expanses management which allows to 
- import expanses from your bank
- review expanses 
- manage categories and tags
- automatically assign categories based on already categorized records

There is a plan to add an analytical dashboard, however any analytical tool like [Metabase](https://www.metabase.com) could already be used for your budget analytics.

# Install

1. Clone repository
```
git clone https://github.com/ztanis/budget.git
cd budget
```
2. Install requirements
```
pip install -r requirements.txt
```
3. Run application
```
PYTHONPATH=`pwd` SQLALCHEMY_DATABASE_URI=sqlite:///data/budget.db python budget/app.py
```
where `SQLALCHEMY_DATABASE_URI` is a url of db. See more details and options for [sqlalchemy](https://docs.sqlalchemy.org/en/13/core/engines.html).
4. Open in browser: http://localhost:5000/admin/get_started/

# [Optional] Visualise expenses analytics

1. [Install metabase](https://www.metabase.com/docs/latest/operations-guide/installing-metabase.html)
2. [Add Database source](https://www.metabase.com/docs/latest/administration-guide/01-managing-databases.html)
3. [Ask a question about your expenses](https://www.metabase.com/docs/latest/users-guide/04-asking-questions.html)
