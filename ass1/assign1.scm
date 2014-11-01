(define (run1)
  (println "For the if function it will evaluate the following argv and sees if it is true then to excute the second argv, at last it stop. However, for my-if function which is almost extractly same except when a=0, it will do the third which is (/ x a). Then the function will have a error which is division‘s denominator cannot be o.")
)
;============================================

(define (zeno_cost d c f)
  (cond
  ((<= c (/ (real 1) 12))
    0)
  ((<= d (/ (real 1) 9600))
      5)
  (else ;Ben gave me a idea about recur case
    (+ (zeno_cost (/ (real d) 2) (* c f) f) c)
        )
      )
  )

(define (run2)
  (print "The answer is " (zeno_cost (/ 2.5 9600) 10 10))
  (println "[it should be 115]") 
)

;==========================================================
(define (min8 a b c d e f g h)
  (define (compare x y)
    (if (<= x y)
        x
        y
    )
  )
  (compare h (compare g (compare f (compare e (compare d (compare c (compare b a)))))))
)

(define (run3)
  (println "minimum is " (min8 10 4 3 9 5 6 7 8))
  (println "[It compared 7 times]")
  (println "minimum is " (min8 1 4 3 19 5 16 7 8))
  (println "[It compared 7 times]")
  )

;============================================================

(define (root3 n)
  (define (iter max min guess)
    (cond
      ((< (* guess guess guess) n)
       (iter max guess (/ (real (+ guess max)) 2))
       )
      ((> (* guess guess guess) n)
       (iter guess min (/ (real (+ guess min)) 2))
       )
      (else
        guess)
    )
    )
    (iter (+ n 1) 0 1)
  )

(define (run4)
  (println "n = 27, The root is " (root3 27) " The answer should 3.")
  (println "n = 64, The root is " (root3 64) " The answer should 4.")
  (println "n = 8, The root is " (root3 8) " The answer should 2.")

  )
;=======================================================================
;Ben helped me to find the print stuff function
(define (pt row)

(define (printSpace count)
  (cond
    ((= count 0) (print " "))
    (else (printSpace (- count 1))
          (print " ")))
    )

(define (printT l)
  (cond
    ((null? l) 1)
    (else (print (car l) " ")
          (printT (cdr l))
          )
    )
  )

(define (printList l count)
  (cond
    ((null? l) 1)
    (else (printSpace count) (printT (car l))
          (println)
          (printList (cdr l) (- count 1))
      )
    )
  )

(define (helper row tempList)
  (define (iter colCount l)
    (define (pascal row col)
      (cond
        ((or (= row col) (= 1 col))
      1)
      (else (+ (pascal (- row 1) (- col 1)) (pascal (- row 1) col)) )
      )
    )
  (if (= colCount 0)
      l
      (iter (- colCount 1) (cons (pascal (+ row 1) colCount) l))
      ))
  (cond
  ((= row -1)
   tempList
   )
   (else (helper (- row 1) (cons (iter (+ row 1) ()) tempList)))
    )
)
(printList (helper row ()) row)
)



(define (run5)
  (println "row = 1 the PT is ")
  (print (pt 1))
  (println "row = 13 the PT is ")
  (print (pt 13))
  (println "row = 9 the PT is ")
  (print (pt 9))
  )

;=========================================================================
(define (zorp i f)
  (define (iter x y z count)
    ;got this iterative idea from Kaleb and Dr.j
    ;it has 3 base cases and shift to right with box like fib's doing
        (cond
            ((= count 0)
                x)
            ((= count 1)
                y)
            ((= count 2)
                z)
            (else
                (iter y z (+ z (/ (* (- z y) (- z y)) (+ (- x (* 2 y)) z))) (- count 1))
                )
            )
        )
    (iter (f 0) (f 1) (f 2) i)
    )
(define (run6)
  (println "iter: " (zorp 2 (lambda (x) (* x x))) " It should be 4")
  (println "iter: " (zorp 0 (lambda (x) (* x x))) " It should be 0")
  (println "iter: " (zorp 1 (lambda (x) (* x x))) " It should be 1")
  (println "iter: " (zorp 6 (lambda (x) (* x x))) " It should be 133")

  )

;=============================================================================

(define (square i)
  (define (iter count result)
    (cond
      ((= count 1)
       result)
      (else
        (iter (- count 1) (- (+ (+ result count) count) 1))
      )
    )
    )
  (iter i 1)
  )

(define (halve x)
  (define (iter count odd even)
  (cond
    ((= count 1);The base cases idea I got from Kaleb
     odd)
    ((= count 2)
     even)
    (else
      (iter (- count 2) (+ odd 1) (+ even 1)))
    )
  )
  (iter x 0.5 1)
  )

(define (babyl* a b)
  (halve (- (- (square (+ a b)) (square a)) (square b)))
    )

(define (run7)
  (println "a = 1, b = 1. The answer should be 1." " " "The babyl* calculate answer is " (babyl* 1 1))
  (println "a = 4, b = 5. The answer should be 20." " " "The babyl* calculate answer is " (babyl* 4 5))

  )


;================================================================================

(define (ecf terms)
    (define (recur i)
      (cond
      ((> i terms)
            0)
      (else ;Kaleb gave me the recur idea
        (/ 1 (+ 1 (/ 1 (+ (* i 2) (/ (real 1) (+ 1 (recur (+ i 1))))))))
            )
        )
      )
    (+ 2 (recur 1))
    )

(define (run8)
  (println (ecf 1) " ecf(1) should be 2.75")
  (println (ecf 2) " ecf(2) should be 2.717948717")
  (println (ecf 3) " ecf(3) should be 2.718284")
  (println (ecf 4) " ecf(4) should be 2.718282")
  (println (ecf 5) " ecf(5) should be 2.718282")
  )
;================================================================================

(define (ramanujan depth)
  (define (iter count result)
    (cond
      ((= count 0)
       result)
      (else
        (iter (- count 1) (sqrt (+ 1 (* (+ count 1) result))))
      )
    )
    )
  (cond
    ((= 0 depth)
     1)
    ((= 1 depth)
     (sqrt 3))
    (else 
      (iter (- depth 1) (sqrt (+ 1 (+ depth 1)))))
    )    
  )       
         
        

(define (run9)
  (println "pass depth = 0 it should be 0....... " (ramanujan 0) )
  (println "Pass depth = 1 it should be 1.73....  " (ramanujan 1) )
  (println "pass depth = 2 it should be 2.23.... " (ramanujan 2) )
  (println "pass depth = 3 it should be 2.55.... " (ramanujan 3) )
  (println "pass depth = 4 it should be 2.755.... " (ramanujan 4) )
  ) 
;===================================================================================

(define (ramanujan2 depth x)
  (define (recur count)
    (cond
      ((= count depth)
       1)
      (else
      (sqrt (+ 1 (* (recur (+ count 1)) (+ x count)))));Kaleb helped me to think the recur case.
      )
    )
    (recur 0)
  )
(define (run10)
(println "(ramanujan2 4 4) " (ramanujan2 4 4))
(println "[It should be 4.454771]")
(println "(ramanujan2 2 3) " (ramanujan2 2 3))
(println "[It should be 2.776365]")
)                                   
;====================================================================================
;(run1)
;(run2)
;(run3)
;(run4)
;(run5)
;(run6)
;(run7)
;(run8)
;(run9)
;(run10)
(println "assignment 1 loaded!")
