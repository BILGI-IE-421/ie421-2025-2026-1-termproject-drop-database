[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/PlHXFZE7)
IE 421 - Data Science for Engineers Term Project
The Asymptote of Olympic Glory
This repository presents a comprehensive data science analysis exploring the biological and cultural limits of human athletic performance through 120 years of Olympic history (1896-2020). Using advanced statistical modeling and extreme value theory, we investigate whether humanity is approaching the mathematical ceiling of physical achievement, and examine the cultural factors that determine Olympic dominance in this era of converging performance.
The project reveals that human performance has reached approximately 99% of biological capacity across major Olympic sports, with future improvements measured in millimeters and milliseconds rather than breakthrough achievements. Through regression analysis, performance saturation indices, and cultural correlation studies, we demonstrate how the Olympics have transitioned from an era of human expansion to one of human convergence—approaching the asymptote of what is physically possible.
Course: IE 421 - Data Science for Engineers
Institution: Istanbul Bilgi University
Term: 2025-2026 Fall Semester
ID / NAME
121203076 -- Yiğit Şamil Ercedoğan
122203053 -- Batuhan Sarı
122203016 -- İlhan Uysal
120203025 -- Ali Baran Turan
121203041 -- Efe Odabaşı

Files
Data Files

data/: Contains Olympic historical datasets spanning 1896-2020

olympic_records.csv: Performance records across track & field, swimming, and gymnastics
athlete_demographics.csv: Age, nationality, and medal data for all Olympic medalists
cultural_indices.csv: Hofstede's Individualism Index scores correlated with GDP and population



Visualizations

visuals/: Includes all generated visualization images used in the analysis

gender_participation.png: Historical trends in male vs. female Olympic participation rates
performance_saturation_100m.png: Asymptotic modeling of 100m sprint records showing biological limit convergence
performance_saturation_swimming.png: Swimming performance trends demonstrating saturation effects
individualism_medals.png: Correlation between cultural individualism scores and medal counts
mean_age_trend_graph.png: Evolution of average athlete age across three historical eras (1900-2020)
olimpiyat_1.jpeg, Olimpiyat2.jpeg: Background images for hero and section designs



Scripts

scripts/: Python scripts for data analysis, statistical modeling, and visualization generation

data_preprocessing.py: Cleans and prepares Olympic datasets for analysis
performance_modeling.py: Implements OLS log-linear regression and Extreme Value Theory (EVT) models
saturation_analysis.py: Calculates Performance Saturation Index (PSI) and detects asymptotic limits
cultural_correlation.py: Analyzes Hofstede scores against medal counts with GDP/population controls
visualization_generator.py: Creates all charts and graphs used in the final presentation
age_breakpoint_detection.py: Performs Chow tests and structural break analysis on athlete age distributions



Web Interface

index.html: Main interactive webpage for GitHub Pages hosting, featuring:

Responsive design with smooth scrolling navigation
Three research questions with data visualizations
Methodology and conclusion sections
Animated transitions and parallax effects



Hosting
The project is hosted using GitHub Pages at:
Live Demo: https://bilgi-ie-421.github.io/ie421-2025-2026-1-termproject-drop-database/

Research Questions Explored

Are we approaching the biological limits of human performance?

Analysis of 100m sprint and swimming records using asymptotic modeling
Performance Saturation Index (PSI) calculations showing 99% capacity utilization


Does culture predict Olympic success more than resources?

Hofstede's Individualism Index correlated with medal counts
Controls for GDP per capita and population size


How has the age structure of elite athletes evolved?

Three-era analysis: Turbulence (1900-1950), Youth Focus (1950-1980), Veteran Rise (1980-present)
Structural break detection showing professionalization and medical advancement effects




