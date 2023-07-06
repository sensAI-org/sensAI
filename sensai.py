from transformers import pipeline
import sys
import csv
from progress.bar import ChargingBar

sentiment_analysis = pipeline("sentiment-analysis",model="siebert/sentiment-roberta-large-english")

def main():
    lpass = True
    print(sys.argv)

    # Handling arguments
    if len(sys.argv) == 2:
        input_file_name = sys.argv[1]
    elif len(sys.argv) == 1:
        input_file_name = "test-reviews.csv"
    else:
        lpass = False
        # file and AI handling



    if lpass:
        
        print

        output_file = open("output.csv", "w")
        with open(input_file_name, "r", encoding='UTF8', newline='') as input_file:
            data = input_file.readlines()
            writer =  csv.writer(output_file)
            bar = ChargingBar("Processing...", max=len(data))
            for line in data:
                score = sentiment_analysis(line)
                rating = 0
                if score[0]["label"] == "NEGATIVE":
                    rating = 1 - float(score[0]["score"])
                else:
                    rating = float(score[0]["score"])
                
                data = [line[:-2], rating, score[0]["label"]]
                bar.next()
                writer.writerow(data)
    else:
        print("\033[93mYou have provided too few or too many parameters!\nPlease try again or refer to the documentation.\033[93m")

if __name__ == "__main__":
    main()