from datetime import datetime
class Constants:

    labCutoffs = {	"Assignment 0"	:	datetime.strptime( "Aug 01 2030 17:45:00", "%b %d %Y %H:%M:%S" ),
                    "Assignment 1"	:	datetime.strptime( "Jan 31 2018 17:45:00", "%b %d %Y %H:%M:%S" ),
                    "Assignment 2"	:	datetime.strptime( "Feb 07 2018 17:45:00", "%b %d %Y %H:%M:%S" ),
                    "Assignment 3"	:	datetime.strptime( "Feb 21 2018 17:45:00", "%b %d %Y %H:%M:%S" ),
                    "Assignment 5"	:	datetime.strptime( "Feb 28 2018 17:45:00", "%b %d %Y %H:%M:%S" ),
                    "Assignment 6"	:	datetime.strptime( "Mar 06 2018 17:45:00", "%b %d %Y %H:%M:%S" ),
                    "Assignment 7"	:	datetime.strptime( "Mar 21 2018 17:45:00", "%b %d %Y %H:%M:%S" ),
                    "Assignment 8"	:	datetime.strptime( "Apr 04 2018 17:45:00", "%b %d %Y %H:%M:%S" ),
                    "Assignment 10"	:	datetime.strptime( "Apr 11 2018 17:45:00", "%b %d %Y %H:%M:%S" ),
                    "Assignment 11" :   datetime.strptime( "Apr 18 2018 17:45:00", "%b %d %Y %H:%M:%S" ),
                    "Assignment 12" :   datetime.strptime( "Apr 25 2018 17:45:00", "%b %d %Y %H:%M:%S" )
    }

    #Section 1 cutoff at 2:40pm on lab due day, extra 10 min for leeway
    labCutoffsSecA = { "Assignment 0"	:	datetime.strptime( "Aug 01 2030 17:45:00", "%b %d %Y %H:%M:%S" ),
                    "Assignment 1"	:	datetime.strptime( "Jan 31 2018 14:40:00", "%b %d %Y %H:%M:%S" ),
                    "Assignment 2"	:	datetime.strptime( "Feb 07 2018 14:40:00", "%b %d %Y %H:%M:%S" ),
                    "Assignment 3"	:	datetime.strptime( "Feb 21 2018 14:40:00", "%b %d %Y %H:%M:%S" ),
                    "Assignment 5"	:	datetime.strptime( "Feb 28 2018 14:40:00", "%b %d %Y %H:%M:%S" ),
                    "Assignment 6"	:	datetime.strptime( "Mar 06 2018 14:40:00", "%b %d %Y %H:%M:%S" ),
                    "Assignment 7"	:	datetime.strptime( "Mar 21 2018 14:40:00", "%b %d %Y %H:%M:%S" ),
                    "Assignment 8"	:	datetime.strptime( "Apr 04 2018 14:40:00", "%b %d %Y %H:%M:%S" ),
                    "Assignment 10"	:	datetime.strptime( "Apr 11 2018 14:40:00", "%b %d %Y %H:%M:%S" ),
                    "Assignment 11" :   datetime.strptime( "Apr 18 2018 14:40:00", "%b %d %Y %H:%M:%S" ),
                    "Assignment 12" :   datetime.strptime( "Apr 25 2018 14:40:00", "%b %d %Y %H:%M:%S" )
    }

    #Section 2 cutoff at 4:10pm on lab due day, extra 10 min for leeway
    labCutoffsSecB = { "Assignment 0"	:	datetime.strptime( "Aug 01 2030 17:45:00", "%b %d %Y %H:%M:%S" ),
                    "Assignment 1"	:	datetime.strptime( "Jan 31 2018 16:10:00", "%b %d %Y %H:%M:%S" ),
                    "Assignment 2"	:	datetime.strptime( "Feb 07 2018 16:10:00", "%b %d %Y %H:%M:%S" ),
                    "Assignment 3"	:	datetime.strptime( "Feb 21 2018 16:10:00", "%b %d %Y %H:%M:%S" ),
                    "Assignment 5"	:	datetime.strptime( "Feb 28 2018 16:10:00", "%b %d %Y %H:%M:%S" ),
                    "Assignment 6"	:	datetime.strptime( "Mar 06 2018 16:10:00", "%b %d %Y %H:%M:%S" ),
                    "Assignment 7"	:	datetime.strptime( "Mar 21 2018 16:10:00", "%b %d %Y %H:%M:%S" ),
                    "Assignment 8"	:	datetime.strptime( "Apr 04 2018 16:10:00", "%b %d %Y %H:%M:%S" ),
                    "Assignment 10"	:	datetime.strptime( "Apr 11 2018 16:10:00", "%b %d %Y %H:%M:%S" ),
                    "Assignment 11" :   datetime.strptime( "Apr 18 2018 16:10:00", "%b %d %Y %H:%M:%S" ),
                    "Assignment 12" :   datetime.strptime( "Apr 25 2018 16:10:00", "%b %d %Y %H:%M:%S" )
    }

    #Section 3 cutoff at 5:40pm on lab due day, extra 10 min for leeway
    labCutoffsSecC = { "Assignment 0"	:	datetime.strptime( "Aug 01 2030 17:45:00", "%b %d %Y %H:%M:%S" ),
                    "Assignment 1"	:	datetime.strptime( "Jan 31 2018 17:40:00", "%b %d %Y %H:%M:%S" ),
                    "Assignment 2"	:	datetime.strptime( "Feb 07 2018 17:40:00", "%b %d %Y %H:%M:%S" ),
                    "Assignment 3"	:	datetime.strptime( "Feb 21 2018 17:40:00", "%b %d %Y %H:%M:%S" ),
                    "Assignment 5"	:	datetime.strptime( "Feb 28 2018 17:40:00", "%b %d %Y %H:%M:%S" ),
                    "Assignment 6"	:	datetime.strptime( "Mar 06 2018 17:40:00", "%b %d %Y %H:%M:%S" ),
                    "Assignment 7"	:	datetime.strptime( "Mar 21 2018 17:40:00", "%b %d %Y %H:%M:%S" ),
                    "Assignment 8"	:	datetime.strptime( "Apr 04 2018 17:40:00", "%b %d %Y %H:%M:%S" ),
                    "Assignment 10"	:	datetime.strptime( "Apr 11 2018 17:40:00", "%b %d %Y %H:%M:%S" ),
                    "Assignment 11" :   datetime.strptime( "Apr 18 2018 17:40:00", "%b %d %Y %H:%M:%S" ),
                    "Assignment 12" :   datetime.strptime( "Apr 25 2018 17:40:00", "%b %d %Y %H:%M:%S" )
    }

    columnIDs = {
                    "Assignment 1"	:	"1271854",
                    "Assignment 2"	:	"1271872",
                    "Assignment 3"	:	"1271871",
                    "Assignment 5"	:	"1271870",
                    "Assignment 6"	:	"1271869",
                    "Assignment 7"	:	"1271868",
                    "Assignment 8"	:	"1271867",
                    "Assignment 10"	:	"1271866",
                    "Assignment 11"	:	"1271865",
                    "Assignment 12" :   "1271864",
                    "Assignment 0"  :   "0000000",
                    "Studio 0"      :   "1272336",
                    "Studio 1"      :   "1272335",
                    "Studio 2"      :   "1272334",
                    "Studio 3"      :   "1272333",
                    "Studio 4"      :   "1272332",
                    "Studio 5"      :   "1272331",
                    "Studio 6"      :   "1272330",
                    "Studio 7"      :   "1272329",
                    "Studio 8"      :   "1272328",
                    "Studio 10"     :   "1272327",
                    "Studio 11"     :   "1272326",
                    "Studio 12"     :   "1272325"
    }

    maxScore = {
                    "Assignment 1"	:	100.0,
                    "Assignment 2"	:	100.0,
                    "Assignment 3"	:	100.0,
                    "Assignment 5"	:	100.0,
                    "Assignment 6"	:	100.0,
                    "Assignment 7"	:	100.0,
                    "Assignment 8"	:	100.0,
                    "Assignment 10"	:	100.0,
                    "Assignment 11"	:	100.0,
                    "Assignment 12" :   100.0,
                    "Assignment 0"  :   0.0
    }

    # Constants relating to parsing lab grade submissions
    labPartnerFields = [["partner_1_student_id_(6_digit_number)", "partner_1_wustl_id_(the_6_digit_number)"], ["partner_2_student_id_(6_digit_number)", "partner_2_wustl_id_(the_6-digit_number)"]]
    labWorkingWithPartner = "are_they_working_with_a_partner?"
    labCommitToGithub = "commit_to_github"
    labTAName = "ta_name"
    labStartTime = "start_time"
    labNonGradingFields = {
        "partner_1_wustl_key",
        "partner_2_wustl_key", 
        "partner_1_student_id_(6_digit_number)", 
        "partner_1_wustl_id_(the_6_digit_number)", 
        "partner_2_student_id_(6_digit_number)", 
        "partner_2_wustl_id_(the_6-digit_number)",
        "completion_time", 
        "ta_name", 
        "email", 
        "are_they_working_with_a_partner?", 
        "commit_to_github",
        "is_this_a_regrade?",
        "start_time",
        "name"
    }

    # Constants relating to parsing studio submissions
    studioPartnerFields = ["student_one_student_id_(6_digit_number)", "student_two_student_id_(6_digit_number)", "student_three_student_id_(6_digit_number)", "student_four_student_id_(6_digit_number)"]
    studioTAName = "ta_name"
    studioStartTime = "start_time"
    # labNonGradingFields = {
    #     "partner_1_wustl_key",
    #     "partner_2_wustl_key", 
    #     "completion_time", 
    #     "ta_name", 
    #     "email", 
    #     "are_they_working_with_a_partner?", 
    #     "commit_to_github",
    #     "start_time",
    #     "name"
    # }