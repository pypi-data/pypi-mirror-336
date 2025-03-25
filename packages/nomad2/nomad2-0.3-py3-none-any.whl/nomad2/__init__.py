def os():
    print(""" 
           
           1.Banker
           2.Needsafe
           3.Processgrant
           4.Linked
           5.Index
           6.Sequential
           7.Scan
           8.Cscan
           9.Look
           10.Clook
           11.Fcfs
           12.Sstf
           13.Mpis
           14.Mpim
           15.Mpie
    
    
    """)


def Banker():
    print("""
    
            //slip no 1,4,11
            /*Write a c menu driven program to implement following functionality
            a)Accept available
            b)Display Allocation,Max
            c)Display the content of Need Matrix
            d)Display Available*/





            #include <stdio.h>

            #define P 5  
            #define R 3  

            int main() {
                int allocation[P][R] = {
                    {2, 3, 2},
                    {4, 0, 0},
                    {5, 0, 4},
                    {4, 3, 4},
                    {2, 2, 4}
                };

                int max[P][R] = {
                    {9, 7, 5},
                    {5, 2, 2},
                    {1, 0, 4},
                    {4, 4, 4},
                    {6, 5, 5}
                };

                int available[R] = {3, 3, 2};

                int need[P][R];
                int choice;

                
                for (int i = 0; i < P; i++) {
                    for (int j = 0; j < R; j++) {
                        need[i][j] = max[i][j] - allocation[i][j];
                    }
                }

                do {
                    printf("\nMenu:\n");
                    printf("1. Accept Available\n");
                    printf("2. Display Allocation and Max\n");
                    printf("3. Display Need Matrix\n");
                    printf("4. Display Available\n");
                    printf("5. Exit\n");
                    printf("Enter your choice: ");
                    scanf("%d", &choice);

                    switch (choice) {
                        case 1:
                            printf("\nEnter Available Resources (A B C): ");
                            for (int i = 0; i < R; i++) {
                                scanf("%d", &available[i]);
                            }
                            break;

                        case 2:
                            printf("\nAllocation and Max:\n");
                            printf("Process\tAllocation\tMax\n");
                            for (int i = 0; i < P; i++) {
                                printf("P%d\t", i);
                                for (int j = 0; j < R; j++)
                                    printf("%d ", allocation[i][j]);
                                printf("\t");
                                for (int j = 0; j < R; j++)
                                    printf("%d ", max[i][j]);
                                printf("\n");
                            }
                            break;

                        case 3:
                            printf("\nNeed Matrix:\n");
                            printf("Process\tNeed\n");
                            for (int i = 0; i < P; i++) {
                                printf("P%d\t", i);
                                for (int j = 0; j < R; j++) {
                                    printf("%d ", need[i][j]);
                                }
                                printf("\n");
                            }
                            break;

                        case 4:
                            printf("\nAvailable Resources: ");
                            for (int i = 0; i < R; i++) {
                                printf("%d ", available[i]);
                            }
                            printf("\n");
                            break;

                        case 5:
                            printf("\nExiting...\n");
                            break;

                        default:
                            printf("\nInvalid choice, try again.\n");
                    }
                } while (choice != 5);

                return 0;
            }




    
    """)



def Needsafe():
    print("""
    
            //Slip No 3,13,19,24,26

            /*Q1)Write a c program to simulate Banker's algorithm for the purpose of deadlock avoidance.Consider the following snapshot of system. A,B,C and D is the resourse type.

            a)Calculate and display the content of need matrix ?
            b)Is the system in safe state? If display the safe sequence.*/




            #include <stdio.h>
            #include <stdbool.h>

            #define P 5  
            #define R 4  

            int main() {
                int allocation[P][R] = {
                    {0, 0, 1, 2},
                    {1, 0, 0, 0},
                    {1, 3, 5, 4},
                    {0, 6, 3, 2},
                    {0, 0, 1, 4}
                };

                int max[P][R] = {
                    {0, 0, 1, 2},
                    {1, 7, 5, 0},
                    {2, 3, 5, 6},
                    {0, 6, 5, 2},
                    {0, 6, 5, 6}
                };

                int available[R] = {1, 5, 2, 0};
                int need[P][R];

                
                for (int i = 0; i < P; i++) {
                    for (int j = 0; j < R; j++) {
                        need[i][j] = max[i][j] - allocation[i][j];
                    }
                }

                
                printf("\nNeed Matrix:\n");
                printf("Process\tA B C D\n");
                for (int i = 0; i < P; i++) {
                    printf("P%d\t", i);
                    for (int j = 0; j < R; j++) {
                        printf("%d ", need[i][j]);
                    }
                    printf("\n");
                }

                
                bool finish[P] = {false};
                int safeSequence[P];
                int work[R];

                
                for (int i = 0; i < R; i++) {
                    work[i] = available[i];
                }

                int count = 0;

                while (count < P) {
                    bool found = false;

                    for (int i = 0; i < P; i++) {
                        if (!finish[i]) {
                            bool canAllocate = true;

                            for (int j = 0; j < R; j++) {
                                if (need[i][j] > work[j]) {
                                    canAllocate = false;
                                    break;
                                }
                            }

                            if (canAllocate) {
                                for (int j = 0; j < R; j++) {
                                    work[j] += allocation[i][j];
                                }

                                safeSequence[count++] = i;
                                finish[i] = true;
                                found = true;
                            }
                        }
                    }

                    if (!found) {
                        printf("\nThe system is not in a safe state.\n");
                        return 0;
                    }
                }

                
                printf("\nThe system is in a safe state.\n");
                printf("Safe Sequence: ");
                for (int i = 0; i < P; i++) {
                    printf("P%d", safeSequence[i]);
                    if (i < P - 1) printf(" -> ");
                }
                printf("\n");

                return 0;
            }

    
    """)




def Processgrant():
    print("""
            //Slip No 5,23

            /*Q1) Consider the system with 'm' processes and 'n' resourse types. Accept number of instances of every resource type. For each process accept the allocation and maximum requirement matrices. Write a program to display the conntents of need matrix and to check if the given request of a process can be granted immediately or not.*/ 





            #include <stdio.h>
            #include <stdbool.h>

            int main() {
                int m, n;  

                
                printf("Enter the number of processes: ");
                scanf("%d", &m);
                printf("Enter the number of resources: ");
                scanf("%d", &n);

                int allocation[m][n], max[m][n], need[m][n], available[n];

                
                printf("\nEnter the number of available instances for each resource:\n");
                for (int i = 0; i < n; i++) {
                    printf("Resource %d: ", i + 1);
                    scanf("%d", &available[i]);
                }

                
                printf("\nEnter the Allocation matrix:\n");
                for (int i = 0; i < m; i++) {
                    printf("Process P%d: ", i);
                    for (int j = 0; j < n; j++) {
                        scanf("%d", &allocation[i][j]);
                    }
                }

                
                printf("\nEnter the Maximum requirement matrix:\n");
                for (int i = 0; i < m; i++) {
                    printf("Process P%d: ", i);
                    for (int j = 0; j < n; j++) {
                        scanf("%d", &max[i][j]);
                    }
                }

                
                for (int i = 0; i < m; i++) {
                    for (int j = 0; j < n; j++) {
                        need[i][j] = max[i][j] - allocation[i][j];
                    }
                }

                
                printf("\nNeed Matrix:\n");
                printf("Process\t");
                for (int j = 0; j < n; j++) {
                    printf("R%d ", j + 1);
                }
                printf("\n");

                for (int i = 0; i < m; i++) {
                    printf("P%d\t", i);
                    for (int j = 0; j < n; j++) {
                        printf("%d ", need[i][j]);
                    }
                    printf("\n");
                }

                
                int req[m][n], process;
                printf("\nEnter the process number making the request (0-%d): ", m - 1);
                scanf("%d", &process);

                printf("Enter the request for process P%d:\n", process);
                for (int i = 0; i < n; i++) {
                    printf("Resource %d: ", i + 1);
                    scanf("%d", &req[process][i]);
                }

                
                bool canGrant = true;
                for (int i = 0; i < n; i++) {
                    if (req[process][i] > need[process][i] || req[process][i] > available[i]) {
                        canGrant = false;
                        break;
                    }
                }

                if (canGrant) {
                    printf("\nThe request CAN be granted immediately.\n");
                } else {
                    printf("\nThe request CANNOT be granted immediately.\n");
                }

                return 0;
            }

    
    """)




def Linked():
    print("""
    
            //Slip No 2,6,15,25
            /* Write a program to simulated linked file allocation method.assume disk with n number of block.give value of n as input.randomly mark some block  as allocated and according maintain the list of free b;ock write menu driver program  with menu  options as mentioned below and implement each option
            a)show bit vector
            b)create new file
            c)show directory
            d)exit*/




            #include <stdio.h>
            #include <stdlib.h>
            #include <string.h>

            #define SIZE 100
            #define NEWNODE (struct direntry *)malloc(sizeof(struct direntry))
            #define NEWBLK (struct blknode *)malloc(sizeof(struct blknode))

            struct blknode {
                int bno;
                struct blknode *next;
            };

            struct direntry {
                char fname[14];
                int start, end;
                struct blknode *blist;
                struct direntry *next;
            };

            struct direntry *dirst = NULL, *dirend = NULL;
            int bitvector[SIZE];

            void print_bitvector() {
                for (int i = 0; i < SIZE; i++) {
                    printf("%d ", bitvector[i]);
                }
                printf("\n");
            }

            void create_file() {
                char fname[14];
                int n, i = 0;

                if (dirst == NULL) {
                    dirst = dirend = NEWNODE;
                } else {
                    dirend->next = NEWNODE;
                    dirend = dirend->next;
                }
                dirend->next = NULL;

                printf("\nEnter a filename: ");
                scanf("%s", dirend->fname);
                printf("\nEnter the number of blocks allocated: ");
                scanf("%d", &n);

                dirend->blist = NULL;
                struct blknode *curr = NULL, *prev = NULL;

                while (n > 0) {
                    while (i < SIZE && bitvector[i] != 1) {
                        i++;
                    }

                    if (i >= SIZE) {
                        printf("No free blocks available.\n");
                        return;
                    }

                    curr = NEWBLK;
                    curr->bno = i;
                    curr->next = NULL;

                    if (dirend->blist == NULL) {
                        dirend->start = i;
                        dirend->blist = curr;
                        prev = curr;
                    } else {
                        prev->next = curr;
                        prev = curr;
                    }

                    bitvector[i] = 0;
                    n--;
                    i++;
                }
                dirend->end = i - 1;
            }

            void print_directory() {
                struct direntry *t1;
                struct blknode *curr;

                printf("\nDirectory:\n");
                printf("\nFilename   Start   End\n");

                for (t1 = dirst; t1 != NULL; t1 = t1->next) {
                    printf("%s   %d   %d\n", t1->fname, t1->start, t1->end);
                    printf("Blocks: ");

                    for (curr = t1->blist; curr != NULL; curr = curr->next) {
                        printf("%d ", curr->bno);
                    }
                    printf("\n");
                }
            }

            void delete_file() {
                char fname[14];
                struct direntry *t1 = dirst, *t2 = NULL;
                struct blknode *curr, *prev;

                printf("\nEnter a filename: ");
                scanf("%s", fname);

                while (t1 != NULL && strcmp(t1->fname, fname) != 0) {
                    t2 = t1;
                    t1 = t1->next;
                }

                if (t1 == NULL) {
                    printf("\nFile not found.\n");
                    return;
                }

                for (curr = t1->blist; curr != NULL;) {
                    bitvector[curr->bno] = 1;
                    prev = curr;
                    curr = curr->next;
                    free(prev);
                }

                if (t1 == dirst) {
                    dirst = dirst->next;
                } else {
                    t2->next = t1->next;
                }

                if (dirst == NULL) {
                    dirend = NULL;
                }

                free(t1);
                printf("\nFile deleted successfully.\n");
            }

            int main() {
                int ch1 = 0;

                for (int i = 0; i < SIZE; i++) {
                    bitvector[i] = rand() % 2;
                }

                while (ch1 != 5) {
                    printf("\n1. Print Bit Vector");
                    printf("\n2. Create File");
                    printf("\n3. Print Directory");
                    printf("\n4. Delete File");
                    printf("\n5. Exit");
                    printf("\nEnter your choice: ");
                    scanf("%d", &ch1);

                    switch (ch1) {
                        case 1:
                            print_bitvector();
                            break;
                        case 2:
                            create_file();
                            break;
                        case 3:
                            print_directory();
                            break;
                        case 4:
                            delete_file();
                            break;
                        case 5:
                            printf("\nExiting...\n");
                            exit(0);
                        default:
                            printf("\nInvalid choice. Try again.\n");
                    }
                }

                return 0;
            }

    
    """)




def Index():
    print("""
            //Slip No 17,18
            /*Write a program to simulate Index file allocation assume disk with n number of blocks give value of n as input randomly mark some block as allocated and according maintain the list of free blocks.Write a menu driven program with a menu option as mention above and implement each option.
            a)Show bit vector
            b)Create New File
            c)Show Directory
            d)Delete Directory
            e)Exit*/





            #include <stdio.h>
            #include <stdlib.h>
            #include <string.h>

            #define SIZE 100
            #define NEWNODE (struct directory *)malloc(sizeof(struct directory))

            struct directory {
                char fname[15];
                int ibno, blist[20], k;
                struct directory *next;
            };

            int bitvector[SIZE];

            int main() {
                int ch1 = 0, i, j, n, flag;
                char fname[15];
                struct directory *dirst = NULL, *dirend = NULL, *t1, *t2;

                // Initialize the bit vector with random 0s and 1s
                for (i = 0; i < SIZE; i++) {
                    bitvector[i] = rand() % 2;
                }

                while (ch1 != 5) {
                    printf("\n1. Print Bit Vector");
                    printf("\n2. Create File");
                    printf("\n3. Print Directory");
                    printf("\n4. Delete File");
                    printf("\n5. Exit");
                    printf("\nEnter your choice: ");
                    scanf("%d", &ch1);

                    switch (ch1) {
                        case 1:
                            for (i = 0; i < SIZE; i++)
                                printf("%4d", bitvector[i]);
                            printf("\n");
                            break;

                        case 2:
                            if (dirst == NULL)
                                dirst = dirend = NEWNODE;
                            else {
                                dirend->next = NEWNODE;
                                dirend = dirend->next;
                            }

                            dirend->next = NULL;

                            printf("\nEnter a filename: ");
                            scanf("%s", dirend->fname);
                            printf("\nEnter the number of blocks to allocate: ");
                            scanf("%d", &n);

                            dirend->k = n;
                            i = j = flag = 0;

                            while (n > 0) {
                                if (bitvector[i] == 1) {
                                    if (flag == 0) {
                                        dirend->ibno = i;
                                        flag = 1;
                                    } else {
                                        dirend->blist[j++] = i;
                                    }
                                    bitvector[i] = 0;
                                    n--;
                                }
                                i++;
                            }
                            break;

                        case 3:
                            printf("\nDirectory");
                            printf("\n-----------------------------");
                            printf("\nFilename   Index Block No.   Block List");
                            printf("\n-----------------------------");

                            for (t1 = dirst; t1 != NULL; t1 = t1->next) {
                                printf("\n%s\t%4d\t", t1->fname, t1->ibno);
                                for (j = 0; j < t1->k; j++)
                                    printf("%4d ", t1->blist[j]);
                            }
                            printf("\n-----------------------------");
                            break;

                        case 4:
                            printf("\nEnter a filename: ");
                            scanf("%s", fname);
                            t1 = dirst;
                            t2 = NULL;

                            while (t1 != NULL) {
                                if (strcmp(t1->fname, fname) == 0)
                                    break;
                                t2 = t1;
                                t1 = t1->next;
                            }

                            if (t1 != NULL) {
                                for (j = 0; j < t1->k; j++)
                                    bitvector[t1->blist[j]] = 1;
                                bitvector[t1->ibno] = 1;

                                if (t1 == dirst)
                                    dirst = dirst->next;
                                else
                                    t2->next = t1->next;

                                free(t1);
                                printf("\nFile deleted successfully.\n");
                            } else {
                                printf("\nFile not found.\n");
                            }
                            break;

                        case 5:
                            printf("\nExiting program.\n");
                            break;

                        default:
                            printf("\nInvalid choice. Try again.\n");
                    }
                }

                return 0;
            }

    
    """)



def Sequential():
    print("""
            //Slip No 8,14,16,22
            /*Write a program to simulate contigeous file allocation assume disk with n number of blocks give value of n as input randomly mark some block as allocated and according maintain the list of free blocks.Write a menu driven program with a menu option as mention above and implement each option.
            a)Show bit vector
            b)Create New File
            c)Show Directory
            d)Delete Directory
            e)Exit*/




            #include <stdio.h>
            #include <stdlib.h>
            #include <string.h>
            #include <math.h>

            #define SIZE 100
            #define NEWNODE (struct directory*)malloc(sizeof(struct directory))

            struct directory {
                char fname[14];
                int start, count;
                struct directory *next;
            };

            struct directory *dirst = NULL, *dirend = NULL;
            int bitvector[SIZE];

            int main() {
                int ch1 = 0, i, j, k, n, flag;
                char fname[14];
                struct directory *t1, *t2;

                
                for (i = 0; i < SIZE; i++) {
                    bitvector[i] = rand() % 2;
                }

                while (1) {
                    printf("\n1. Print Bit-vector");
                    printf("\n2. Create File");
                    printf("\n3. Print Directory");
                    printf("\n4. Delete File");
                    printf("\n5. Exit");
                    printf("\nEnter Your Choice: ");
                    scanf("%d", &ch1);

                    switch (ch1) {
                        case 1:
                            for (i = 0; i < SIZE; i++)
                                printf("%d ", bitvector[i]);
                            printf("\n");
                            break;

                        case 2:
                            if (dirst == NULL) {
                                dirst = dirend = NEWNODE;
                            } else {
                                dirend->next = NEWNODE;
                                dirend = dirend->next;
                            }

                            dirend->next = NULL;

                            printf("\nEnter a filename: ");
                            scanf("%s", dirend->fname);

                            printf("Enter the number of blocks allocated: ");
                            scanf("%d", &n);
                            dirend->count = n;

                            for (i = 0; i < SIZE; i++) {
                                if (bitvector[i] == 0) {
                                    for (j = i; j < i + n; j++) {
                                        if (bitvector[j] == 1) {
                                            break;
                                        }
                                    }
                                    if (j == i + n) {
                                        dirend->start = i;
                                        for (k = i; k < j; k++)
                                            bitvector[k] = 1;
                                        break;
                                    }
                                }
                            }
                            if (i == SIZE) {
                                printf("No sufficient space available.\n");
                            }
                            break;

                        case 3:
                            printf("\nDirectory:\n");
                            printf("Filename   Start   Count\n");
                            for (t1 = dirst; t1 != NULL; t1 = t1->next) {
                                printf("%s       %d      %d\n", t1->fname, t1->start, t1->count);
                            }
                            break;

                        case 4:
                            printf("\nEnter a filename to delete: ");
                            scanf("%s", fname);
                            t1 = dirst;
                            t2 = NULL;

                            while (t1 != NULL) {
                                if (strcmp(t1->fname, fname) == 0)
                                    break;
                                t2 = t1;
                                t1 = t1->next;
                            }

                            if (t1 != NULL) {
                                for (i = t1->start; i < t1->start + t1->count; i++)
                                    bitvector[i] = 0;

                                if (t1 == dirst)
                                    dirst = dirst->next;
                                else
                                    t2->next = t1->next;

                                if (t1 == dirend)
                                    dirend = t2;

                                free(t1);
                                printf("\nFile deleted successfully.\n");
                            } else {
                                printf("\nFile not found.\n");
                            }
                            break;

                        case 5:
                            exit(0);
                            break;

                        default:
                            printf("\nInvalid Choice!");
                    }
                }
                return 0;
            }

    
    """)




def Scan():
    print("""
            //Slip No 4,13,18,20
            /*Q)Write a simulation program for disk scheduling using Scan algorithm accept total number of disk block, disk request string and current head position from the user display the list of request in the order in which it is served and display the total number of head movements.
            
            86,147,91,170,95,130,102,70
            Starting Head Position :125
            Direction:Left*/




            #include <stdio.h>
            #include <stdlib.h>

            int main() {
                int n, head, total_blocks, total_head_movements = 0;
                char direction;

                
                printf("Enter the number of disk requests: ");
                scanf("%d", &n);

                total_blocks=n;
                int requests[n + 2];  
                int index = 0;

                
                printf("Enter the disk request sequence:\n");
                for (int i = 0; i < n; i++) {
                    scanf("%d", &requests[i]);
                }

                
                printf("Enter the starting head position: ");
                scanf("%d", &head);

                
                printf("Enter the direction (L for Left, R for Right): ");
                scanf(" %c", &direction);

                
                requests[n] = 0;               
                requests[n + 1] = total_blocks - 1;  
                n += 2;

                
                for (int i = 0; i < n - 1; i++) {
                    for (int j = 0; j < n - i - 1; j++) {
                        if (requests[j] > requests[j + 1]) {
                            int temp = requests[j];
                            requests[j] = requests[j + 1];
                            requests[j + 1] = temp;
                        }
                    }
                }

                
                for (int i = 0; i < n; i++) {
                    if (requests[i] >= head) {
                        index = i;
                        break;
                    }
                }

                printf("\nSequence of request execution: ");

                if (direction == 'L' || direction == 'l') {
                    
                    for (int i = index - 1; i >= 0; i--) {
                        printf("%d ", requests[i]);
                        total_head_movements += abs(head - requests[i]);
                        head = requests[i];
                    }

                    
                    for (int i = index; i < n; i++) {
                        printf("%d ", requests[i]);
                        total_head_movements += abs(head - requests[i]);
                        head = requests[i];
                    }
                } else {
                    
                    for (int i = index; i < n; i++) {
                        printf("%d ", requests[i]);
                        total_head_movements += abs(head - requests[i]);
                        head = requests[i];
                    }

                    
                    for (int i = index - 1; i >= 0; i--) {
                        printf("%d ", requests[i]);
                        total_head_movements += abs(head - requests[i]);
                        head = requests[i];
                    }
                }

                printf("\nTotal head movements: %d\n", total_head_movements);

                return 0;
            }

    
    """)





def Cscan():
    print("""
            //Slip No 6,7,10,15,19
            /*Q)Write a simulation program for disk scheduling using C-Scan algorithm accept total number of disk block, disk request string and current head position from the user display the list of request in the order in which it is served and display the total number of head movements.
            
            86,147,91,170,95,130,102,70
            Starting Head Position :125
            Direction:Left*/





            #include <stdio.h>
            #include <stdlib.h>

            int main() {
                int n, head, total_blocks, total_head_movements = 0;
                char direction;

                
                printf("Enter the number of disk requests: ");
                scanf("%d", &n);
            
                total_blocks=n;
                int requests[n];

                
                printf("Enter the disk request sequence:\n");
                for (int i = 0; i < n; i++) {
                    scanf("%d", &requests[i]);
                }

                
                printf("Enter the starting head position: ");
                scanf("%d", &head);

                
                printf("Enter the direction (L for Left, R for Right): ");
                scanf(" %c", &direction);

                
                for (int i = 0; i < n - 1; i++) {
                    for (int j = 0; j < n - i - 1; j++) {
                        if (requests[j] > requests[j + 1]) {
                            int temp = requests[j];
                            requests[j] = requests[j + 1];
                            requests[j + 1] = temp;
                        }
                    }
                }

                printf("\nSequence of request execution: ");

                if (direction == 'R' || direction == 'r') {
                    // Moving right first
                    int index = 0;
                    while (index < n && requests[index] < head) {
                        index++;
                    }

                    
                    for (int i = index; i < n; i++) {
                        printf("%d ", requests[i]);
                        total_head_movements += abs(head - requests[i]);
                        head = requests[i];
                    }

                    
                    total_head_movements += abs(head - (total_blocks - 1));
                    head = total_blocks - 1;

                    
                    total_head_movements += abs(head - 0);
                    head = 0;

                    
                    for (int i = 0; i < index; i++) {
                        printf("%d ", requests[i]);
                        total_head_movements += abs(head - requests[i]);
                        head = requests[i];
                    }
                } else {
                    
                    int index = n - 1;
                    while (index >= 0 && requests[index] > head) {
                        index--;
                    }

                    
                    for (int i = index; i >= 0; i--) {
                        printf("%d ", requests[i]);
                        total_head_movements += abs(head - requests[i]);
                        head = requests[i];
                    }

                    
                    total_head_movements += abs(head - 0);
                    head = 0;

                    
                    total_head_movements += abs(head - (total_blocks - 1));
                    head = total_blocks - 1;

                    
                    for (int i = n - 1; i > index; i--) {
                        printf("%d ", requests[i]);
                        total_head_movements += abs(head - requests[i]);
                        head = requests[i];
                    }
                }

                printf("\nTotal head movements: %d\n", total_head_movements);

                return 0;
            }

    
    """)




def Look():
    print("""
            //Slip NO 9,17,25,27
            /*Q)Write a simulation program for disk scheduling using Look algorithm accept total number of disk block, disk request string and current head position from the user display the list of request in the order in which it is served and display the total number of head movements.
            
            86,147,91,170,95,130,102,70
            Starting Head Position :125
            Direction:Left*/




            #include <stdio.h>
            #include <stdlib.h>

            int main() {
                int n, head, total_head_movements = 0;
                char direction;

                
                printf("Enter the number of disk requests: ");
                scanf("%d", &n);

                int requests[n];

                
                printf("Enter the disk request sequence:\n");
                for (int i = 0; i < n; i++) {
                    scanf("%d", &requests[i]);
                }

                
                printf("Enter the starting head position: ");
                scanf("%d", &head);

                
                printf("Enter the direction (L for Left, R for Right): ");
                scanf(" %c", &direction);

                
                for (int i = 0; i < n - 1; i++) {
                    for (int j = 0; j < n - i - 1; j++) {
                        if (requests[j] > requests[j + 1]) {
                            int temp = requests[j];
                            requests[j] = requests[j + 1];
                            requests[j + 1] = temp;
                        }
                    }
                }

                
                int index = 0;
                for (int i = 0; i < n; i++) {
                    if (requests[i] >= head) {
                        index = i;
                        break;
                    }
                }

                printf("\nSequence of request execution: ");

                if (direction == 'L' || direction == 'l') {
                    
                    for (int i = index - 1; i >= 0; i--) {
                        printf("%d ", requests[i]);
                        total_head_movements += abs(head - requests[i]);
                        head = requests[i];
                    }

                    
                    for (int i = index; i < n; i++) {
                        printf("%d ", requests[i]);
                        total_head_movements += abs(head - requests[i]);
                        head = requests[i];
                    }
                } else {
                    
                    for (int i = index; i < n; i++) {
                        printf("%d ", requests[i]);
                        total_head_movements += abs(head - requests[i]);
                        head = requests[i];
                    }

                    
                    for (int i = index - 1; i >= 0; i--) {
                        printf("%d ", requests[i]);
                        total_head_movements += abs(head - requests[i]);
                        head = requests[i];
                    }
                }

                printf("\nTotal head movements: %d\n", total_head_movements);

                return 0;
            }

    
    """)





def Clook():
    print("""
            //Slip No 12,28,29
            /*Q)Write a simulation program for disk scheduling using C-Look algorithm accept total number of disk block, disk request string and current head position from the user display the list of request in the order in which it is served and display the total number of head movements.
            
            86,147,91,170,95,130,102,70
            Starting Head Position :125
            Direction:Left*/




            #include <stdio.h>
            #include <stdlib.h>

            int main() {
                int n, head, total_head_movements = 0;
                char direction;

                
                printf("Enter the number of disk requests: ");
                scanf("%d", &n);

                int requests[n];

                
                printf("Enter the disk request sequence:\n");
                for (int i = 0; i < n; i++) {
                    scanf("%d", &requests[i]);
                }

                
                printf("Enter the starting head position: ");
                scanf("%d", &head);

                
                printf("Enter the direction (L for Left, R for Right): ");
                scanf(" %c", &direction);

                
                for (int i = 0; i < n - 1; i++) {
                    for (int j = 0; j < n - i - 1; j++) {
                        if (requests[j] > requests[j + 1]) {
                            int temp = requests[j];
                            requests[j] = requests[j + 1];
                            requests[j + 1] = temp;
                        }
                    }
                }

                
                int index = 0;
                for (int i = 0; i < n; i++) {
                    if (requests[i] >= head) {
                        index = i;
                        break;
                    }
                }

                printf("\nSequence of request execution: ");

                if (direction == 'R' || direction == 'r') {
                    
                    for (int i = index; i < n; i++) {
                        printf("%d ", requests[i]);
                        total_head_movements += abs(head - requests[i]);
                        head = requests[i];
                    }
                    
                    total_head_movements += abs(head - requests[0]);
                    head = requests[0];

                    
                    for (int i = 0; i < index; i++) {
                        printf("%d ", requests[i]);
                        total_head_movements += abs(head - requests[i]);
                        head = requests[i];
                    }
                } else {
                    
                    for (int i = index - 1; i >= 0; i--) {
                        printf("%d ", requests[i]);
                        total_head_movements += abs(head - requests[i]);
                        head = requests[i];
                    }
                    
                    total_head_movements += abs(head - requests[n - 1]);
                    head = requests[n - 1];

                    
                    for (int i = n - 1; i >= index; i--) {
                        printf("%d ", requests[i]);
                        total_head_movements += abs(head - requests[i]);
                        head = requests[i];
                    }
                }

                printf("\nTotal head movements: %d\n", total_head_movements);

                return 0;
            }

    
    """)




def Fcfs():
    print("""
            //Slip No 1,21,26,30
            /*Q)Write a simulation program for disk scheduling using FCFS algorithm accept total number of disk block, disk request string and current head position from the user display the list of request in the order in which it is served and display the total number of head movements.
            
            86,147,91,170,95,130,102,70
            Starting Head Position :125
            Direction:Left*/





            #include<stdio.h>
            #include<stdlib.h>
            #include<math.h>

            int main()
            {
                int i,n,request[20],cpos,tracks,hmove=0;
                printf("\n How many request:");
                scanf("%d",&n);
                printf("\n Enter request Array:");
                for(i=0;i<n;i++)
                    scanf("%d",&request[i]);
                printf("\n Enter currunt position of the head:");
                scanf("%d",&cpos);
                printf("\n how many tracks:");
                scanf("%d",&tracks);
                for(i=0;i<n;i++)
                {
                    hmove=hmove+abs(cpos-request[i]);
                    cpos=request[i];
                }
                printf("\n Total head movement=%d",hmove);
            }

    
    """)




def Sstf():
    print("""
            //Slip No 8,14,23
            /*Q)Write a simulation program for disk scheduling using SSTF algorithm accept total number of disk block, disk request string and current head position from the user display the list of request in the order in which it is served and display the total number of head movements.
            
            86,147,91,170,95,130,102,70
            Starting Head Position :125
            Direction:Left*/




            #include <stdio.h>
            #include <stdlib.h>
            #include <limits.h>

            int main() {
                int n, head, total_head_movements = 0;


                printf("Enter the number of disk requests: ");
                scanf("%d", &n);

                int requests[n];
                int visited[n];

                
                printf("Enter the disk request sequence:\n");
                for (int i = 0; i < n; i++) {
                    scanf("%d", &requests[i]);
                    visited[i] = 0;  
                }

                
                printf("Enter the starting head position: ");
                scanf("%d", &head);

                printf("\nSequence of request execution: ");

                for (int i = 0; i < n; i++) {
                    int min_distance = INT_MAX;
                    int index = -1;

                    
                    for (int j = 0; j < n; j++) {
                        if (!visited[j]) {
                            int distance = abs(head - requests[j]);
                            if (distance < min_distance) {
                                min_distance = distance;
                                index = j;
                            }
                        }
                    }

                    visited[index] = 1;  
                    total_head_movements += min_distance;
                    head = requests[index];

                    printf("%d ", requests[index]);
                }

                printf("\nTotal head movements: %d\n", total_head_movements);

                return 0;
            }

    
    """)




def Mpis():
    print("""
            //Slip No 3,10,12
            /* Q) Write an MPI program to calculate sum and average of randomly generated 1000 numbers(stored in array) on a cluster */





            #include <stdio.h>
            #include <stdlib.h>
            #include <mpi.h>
            #include <time.h>

            #define SIZE 1000

            int main(int argc, char* argv[]) {
                int rank, size;
                int numbers[SIZE];
                int local_sum = 0, global_sum = 0;
                double average;

                MPI_Init(&argc, &argv);               
                MPI_Comm_rank(MPI_COMM_WORLD, &rank); 
                MPI_Comm_size(MPI_COMM_WORLD, &size); 

                int chunk_size = SIZE / size;         
                int local_array[chunk_size];

                
                if (rank == 0) {
                    srand(time(NULL)); 
                    printf("Randomly generated numbers:\n");
                    for (int i = 0; i < SIZE; i++) {
                        numbers[i] = rand() % 100 + 1;  
                        printf("%d ", numbers[i]);
                        if ((i + 1) % 20 == 0) printf("\n");
                    }
                }

                
                MPI_Scatter(numbers, chunk_size, MPI_INT, local_array, chunk_size, MPI_INT, 0, MPI_COMM_WORLD);

                
                for (int i = 0; i < chunk_size; i++) {
                    local_sum += local_array[i];
                }

                
                MPI_Reduce(&local_sum, &global_sum, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);

                
                if (rank == 0) {
                    average = (double)global_sum / SIZE;
                    printf("\nTotal Sum: %d\n", global_sum);
                    printf("Average: %.2f\n", average);
                }

                MPI_Finalize();
                return 0;
            }															

    
    """)




def Mpim():
    print("""
            //Slip No 5,11,16,20,27,30
            /* Q) Write an MPI program to find max and min number from randomly generated 1000 numbers(stored in array) on a cluster (Hint:USE MPI_REDUCE) */




            #include <stdio.h>
            #include <stdlib.h>
            #include <mpi.h>
            #include <time.h>

            #define SIZE 1000

            int main(int argc, char* argv[]) {
                int rank, size;
                int numbers[SIZE];
                int local_max, local_min;
                int global_max, global_min;

                MPI_Init(&argc, &argv);               
                MPI_Comm_rank(MPI_COMM_WORLD, &rank); 
                MPI_Comm_size(MPI_COMM_WORLD, &size); 

                int chunk_size = SIZE / size;         
                int local_array[chunk_size];

                
                if (rank == 0) {
                    srand(time(NULL));
                    printf("Randomly generated numbers:\n");
                    for (int i = 0; i < SIZE; i++) {
                        numbers[i] = rand() % 1000 + 1;  
                        printf("%d ", numbers[i]);
                        if ((i + 1) % 20 == 0) printf("\n");
                    }
                }

                
                MPI_Scatter(numbers, chunk_size, MPI_INT, local_array, chunk_size, MPI_INT, 0, MPI_COMM_WORLD);

                
                local_max = local_array[0];
                local_min = local_array[0];

                for (int i = 1; i < chunk_size; i++) {
                    if (local_array[i] > local_max) {
                        local_max = local_array[i];
                    }
                    if (local_array[i] < local_min) {
                        local_min = local_array[i];
                    }
                }

                
                MPI_Reduce(&local_max, &global_max, 1, MPI_INT, MPI_MAX, 0, MPI_COMM_WORLD);
                MPI_Reduce(&local_min, &global_min, 1, MPI_INT, MPI_MIN, 0, MPI_COMM_WORLD);

                
                if (rank == 0) {
                    printf("\nGlobal Maximum: %d\n", global_max);
                    printf("Global Minimum: %d\n", global_min);
                }

                MPI_Finalize();
                return 0;
            }

    
    """)



    

def Mpie():
    print("""
            //Slip No 21,22,24,29
            /* Q) Write an MPI program to calculate sum of all even and odd randomly generated 1000 numbers(stored in array) on a cluster */





            #include <stdio.h>
            #include <stdlib.h>
            #include <mpi.h>
            #include <time.h>

            #define SIZE 1000

            int main(int argc, char* argv[]) {
                int rank, size;
                int numbers[SIZE];
                int local_even_sum = 0, local_odd_sum = 0;
                int global_even_sum = 0, global_odd_sum = 0;

                MPI_Init(&argc, &argv);               
                MPI_Comm_rank(MPI_COMM_WORLD, &rank); 
                MPI_Comm_size(MPI_COMM_WORLD, &size); 

                int chunk_size = SIZE / size;         
                int local_array[chunk_size];

                
                if (rank == 0) {
                    srand(time(NULL));
                    printf("Randomly generated numbers:\n");
                    for (int i = 0; i < SIZE; i++) {
                        numbers[i] = rand() % 1000 + 1;  
                        printf("%d ", numbers[i]);
                        if ((i + 1) % 20 == 0) printf("\n");
                    }
                }

                
                MPI_Scatter(numbers, chunk_size, MPI_INT, local_array, chunk_size, MPI_INT, 0, MPI_COMM_WORLD);

                
                for (int i = 0; i < chunk_size; i++) {
                    if (local_array[i] % 2 == 0) {
                        local_even_sum += local_array[i];
                    } else {
                        local_odd_sum += local_array[i];
                    }
                }

                
                MPI_Reduce(&local_even_sum, &global_even_sum, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);
                MPI_Reduce(&local_odd_sum, &global_odd_sum, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);

                
                if (rank == 0) {
                    printf("\nGlobal Sum of Even Numbers: %d\n", global_even_sum);
                    printf("Global Sum of Odd Numbers: %d\n", global_odd_sum);
                }

                MPI_Finalize();
                return 0;
            }

    
    """)