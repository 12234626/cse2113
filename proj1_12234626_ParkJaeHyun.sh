#! /usr/bin/bash

	if (($# == 3)) && [ -f "$1" ] && [ -f "$2" ] && [ -f "$3" ]
then
	echo "***** OSS1 - Project1 *****"
	echo "* StudentID : 12234626    *"
	echo "* Name      : ParkJaeHyun *"
	echo "***************************"

	teams="$1"
	players="$2"
	matches="$3"
	
	while true
	do
		echo
		echo "[MENU]"
		echo "1. Get the data of Heung-Min Son's Current Club, Appearances, Goals, Assists in players.csv"
		echo "2. Get the team data to enter a league position in teams.csv"
		echo "3. Get the Top-3 Attendance matches in mateches.csv"
		echo "4. Get the team's league position and team's top scorer in teams.csv & players.csv"
		echo "5. Get the modified format of date_GMT in matches.csv"
		echo "6. Get the data of the winning team by the largest difference on home stadium in teams.csv & matches.csv"
		echo "7. Exit"

		read -p "Enter your CHOICE (1~7): " choice
		case "$choice" in
			1)
				read -p "Do you want to get the Heung-Min Son's data? (y/N): " choice
				if [ "$choice" == "y" ] 
				then
					awk -F ',' '$1 == "Heung-Min Son" {printf("Team: %s, Apperance: %d, Goal: %d, Assist: %d\n", $4, $6, $7, $8)}' "$players"
				fi
				;;

			2)
				read -p "What do you want to get the team data of league_position? (1~20): " choice
				awk -F ',' -v choice="$choice" '$6 == choice {printf("%d %s %.6f\n", $6, $1, $2 / ($2 + $3 + $4))}' "$teams"
				;;

			3)
				read -p "Do you want to know Top-3 attendance data and average attendance? (y/N): " choice
				if [ "$choice" == "y" ]
				then
					sort -t ',' -k 2 -n -r "$matches" | head -n 3 | awk -F ',' 'BEGIN {printf("*** Top-3 Attendance Match ***\n")} {printf("\n%s vs %s (%s)\n%d %s\n", $3, $4, $1, $2, $7)}'
				fi
				;;

			4)
				read -p "Do you want to get each team's ranking and the highest-scoring player? (y/N): " choice
				if [ "$choice" == "y" ]
				then
					i=0
					tail -n 20 "$teams" | sort -t ',' -k 6 -n | sed 's/,.*//' | while read team
					do
						((++i))
						awk -F ',' -v team="$team" '$4 == team {printf("%s\n", $0)}' "$players" | sort -t ',' -k 7 -n -r | head -n 1 | awk -F ',' -v i="$i" -v team="$team" '{printf("\n%s %s\n%s %s\n", i, team, $1, $7)}'
					done
				fi
				;;

			5)
				read -p "Do you want to modify the format of date? (y/N): " choice
				if [ "$choice" == "y" ]
				then
				 	sed -n '2,11p' "$matches" | sed -E 's/([A-Za-z]+ [0-9]+ [0-9]+) - ([0-9]+:[0-9]+[ap]m).*/echo "$(date -d "\1" +%Y\/%m\/%d) \2"/e'
				fi
				;;

			6)
				IFS=','
				PS3="Enter your team number: "
				select team in $(awk -F ',' 'NR != 1 {printf("%s,", $1)}' "$teams")
				do
					mx=$(awk -F ',' -v team="$team" '$3 == team {printf("%d\n", $5 - $6)}' "$matches" | sort -n -r | head -n 1)
					awk -F ',' -v team="$team" -v mx="$mx" '$3 == team && $5 - $6 == mx {printf("\n%s\n%s %d vs %d %s\n", $1, $3, $5, $6, $4)}' "$matches"

					break
				done
				;;

			7)
				echo "Bye!"

				exit 0
				;;
		esac
	done
else
	echo "usage: $0 file1 file2 file3"
	
	exit 1
fi
