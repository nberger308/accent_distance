This repository contains sample code used in my recent Master's Dissertation "Low-Resource Accent TTS Support via Large Multi-Accent Neural Frontend Pronunciation Knowledge Transfer."

The code was used to quantify the "accent similarity" of 14 accents (with each other accent) modelled simultaneously in a BiLSTM-based Seq2Seq frontend (text to linguistic specification) model, using Levenshtein distance. The purpose of this metric was to evaluate the feasibility of applying "knowledge transfer" to highly dissimilar accent pairs.

The results, depicted as a heat map, are also included for reference.




HEATMAP KEY:

ABC = Abercrave, Wales

ABD1 = Aberdeen, Scotland

CCL1 = County Clare, Ireland

CDF = Cardiff, Wales

EDI = Edinburgh, Scotland

GAM = General American 

GAU = General Australian

GNZ = General New Zealand

LDS = Leeds, England

LDS1 = Leeds, England with no /h/-dropping feature

NYC = New York City, USA

NYC1 = New York City, USA with non-rhotic feature

RPX = British Received Pronunciation

SCA = South Carolina, USA

