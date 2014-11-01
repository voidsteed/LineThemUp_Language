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
;{(define (square i)
  (cond
    ((= i 1)
     1
    )
    (else (- (+ (+ (square (- i 1)) i) i) 1)
          )
  )
  )

(define (halve x)
  (cond
    ((= x 0)
     0
     )
    (else
      (/ (real x) 2)
      )
    )
  );}

(define (babyl* a b)
  (halve (- (- (square (+ a b)) (square a)) (square b)))
    )

(define (run7)
  (println "a = 1, b = 1. The answer should be 1." " " "The babyl* calculate answer is " (babyl* 1 1))
  (println "a = 4, b = 5. The answer should be 20." " " "The babyl* calculate answer is " (babyl* 4 5))

  )

(run7)
