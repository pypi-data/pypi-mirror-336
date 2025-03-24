# sphinx_enos_theme

## Change Log

### 0.3.26

add control enableAuth

### 0.3.5

add toc-tree auth

### 0.2.94

update security
### 0.2.93

update version switch

### 0.2.92

update onlineEdit fix suffix

### 0.2.91

update path with docs

### 0.2.90

back-to-top update time
### 0.2.89

back-to-top update time

### 0.2.88

add search

### 0.2.87

jump 81~86, update header

### 0.2.86

fix global search is hidden in rtd

### 0.2.85

fix global search position and add go back href

### 0.2.84

fix global search in new page

### 0.2.83

fix axios res -> res.data

### 0.2.82

fix search result doSearchFunc res.results -> res

### 0.2.81

fix global search and BE pagination

### 0.2.80

* Collapse and expand the navigation bar

### 0.2.63

* fix new rtd

### 0.2.56

* update seo link

### 0.2.55

* update favicon and logo and footer and jump host

### 0.2.48

* name themeCustom to theme

### 0.2.46

* display dev with condition

### 0.2.45

* tooltip

### 0.2.41

* media layout

### 0.2.37

* enos_gitlab_repo

### 0.2.34

* show_git_lab_editor

### 0.2.33

* display_source

### 0.2.32

* fix h4,h5,h6 font size

### 0.2.31

* fix table bug

### 0.2.30

* add docs home jump

### 0.2.29

* fit variable rules

### 0.2.28

* fit script order

### 0.2.27

* fit header version g_url

### 0.2.26

* fit read the docs and online

### 0.2.25

* add time stamp in src

### 0.2.24

* fix header version dropdown

### 0.2.23

* fix header and footer
* fix logo jump
* fix table layout

### 0.2.14

* add auth
* fix header issue

### 0.2.8

* Add product name
* Move version to header
* hide Dev version

### 0.2.5

* change note css

### 0.2.4

* adjust table css

### 0.2.3

* remove PDF download button

### 0.2.2

* add config display_header default true
* add config copyright_en and copyright_zh
* fix some bug

### 0.2.1

* header update

### 0.1.4

* show image as Full screen mode
* change toc deep to 8
* add about chanel
* fix some language bugs 

### 0.1.3

* Auto scroll to current selected toc
* Add + to the node, if there are any children under it

### 0.1.2 

* Change toc deep to 4
* Hide current page toc from global toc tree
* Fix a small bug 

### 0.1.1 

* Change selected toc style 
* Add PDF download button
* Add version change dropdown list

## Usage: 

```
pip install sphinx_enos_theme
```

Change `conf.py` 

```
html_theme = "sphinx_enos_theme"
```

## Contribute

Use `gulp` `webpack` to compile CSS/JS and HTML template

### Dependencies

* Python >= 2.7
* node >= 9.0
* gulp >= 4.0
* webpack >= 4.0
* sphinx 

### Before development 

> go to src/templates/layout.html, uncomment line 151 & comment line 153

* prepare dev

```
gulp pre
```

* start dev server 

```
gulp
```

### publish new version 

> go to src/templates/layout.html, comment line 151 and uncomment line 153

update the version number in _init_.py

* build dist

```
gulp build
```

* dist python package

```
python setup.py sdist
```

* publish

```
twine upload dist/*
```
