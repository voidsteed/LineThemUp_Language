(define (cons-stream # a $b)
  (cons
    a
    (lambda () (eval $b #))
    )
  )

(define stream-car car)
(define (stream-cdr s)
  ((cdr s))
  )

(define (sdisplay s n)
  (cond
    ((= n 0) (println "..."))
    (else
      (print (stream-car s) " ")
      (sdisplay (stream-cdr s) (- n 1))
      )
    )
  )


(define (display-stream s n)
  (cond
    ((= n 0) (println "..."))
    (else
      (println (stream-car s) " ")
      (display-stream (stream-cdr s) (- n 1))
      )
    )
  )

(define (stream-add s t)
  (cons-stream
    (+ (stream-car s) (stream-car t))
    (stream-add
      (stream-cdr s)
      (stream-cdr t)
      )
   )
  )

(define (stream-map f @)
  (define (iter streams)
    (cons-stream
      (apply f (map stream-car streams))
      (iter (map stream-cdr streams))
      )
    )
  (iter @)
  )
;--------------------------------------------------------
;Ones
(define (ones)
  (cons-stream
    1
    (ones)
    )
  )

;integers
(define (ints) 
  (cons-stream 
    0 
    (stream-add (ones) (ints))
    )
  )
;partial sum
(define (psum s)
  (cons-stream
    (stream-car s)
    (stream-add
      (stream-cdr s)
      (psum s)
      )
    )
  )
;--------------------------------------
;addsum problem 5

(define (addsub s)
  (cons-stream
    (stream-car s)
    (stream-add
      (stream-cdr s)
      (addsub s)
      )
   )
  )

(define (alt s)
  (define alt-ones
    (cons-stream
      1
      (cons-stream -1 alt-ones)))
  (stream-map * s alt-ones)
  )

(define x (alt (ints)))
;(sdisplay x 10)

(define z (addsub x))

(define (run5)
  (print "The numeric stream result is: " )
  (sdisplay z 10)
  (println "It should be 0 -1 1 -2 2 -3 3 -4 4 -5 ...")
  )

(run5)
;-----------------------Pro7--------------------
(define (stream-ref s n)
  (cond
    ((= n 0) 
     (stream-car s))
    (else
      (stream-ref (stream-cdr s) (- n 1))
  )))

(define (square x)
  (expt x 2))

(define (euler-transform s)
  (let ((s0 (stream-ref s 0))
        (s1 (stream-ref s 1))
        (s2 (stream-ref s 2)))
  (cond  
    ((= (+ s0 s2) (* 2 s1))
     s)
     (else
       (cons-stream (- s2 (/ (square (- s2 s1))
                        (+ s0 (* -2 s1) s2)))
               (euler-transform (stream-cdr s))))
      ))
)
;(define (pi-summands n)
;  (cons-stream (/ 1.0 n)
;               (stream-map - (pi-summands (+ n 2)))))

;(define c (pi-summands 1))
;(sdisplay c 10)

(define (log-summands n)
  (cons-stream (/ 1.0 n)
               (stream-map - (log-summands (+ n 1)))))

(define ln2
           (psum (log-summands 1)))

;(display-stream ln2 50)
;-------------------------------------
(define aln2 (euler-transform ln2))

;(display-stream aln2 20)
;------------------------------------

(define (make-tableau transform s)
  (cons-stream s
               (make-tableau transform
                     (transform s))))

(define (acc-seq transform s)
  (stream-map stream-car
              (make-tableau transform s)))

(define saln2 (acc-seq euler-transform ln2))
;(display-stream saln2 10)

(define (run7)
  (println "----------------------------------------------------------------------------------")
  (println "---------------------unaccelarate ln2---------------------------------------------")
  (println "----------------------------------------------------------------------------------")
  (display-stream ln2 100)
  (println "----------------------------------------------------------------------------------")
  (println "---------------------accelarated ln2----------------------------------------------")
  (println "----------------------------------------------------------------------------------")
  (display-stream aln2 30)
  (println "----------------------------------------------------------------------------------")
  (println "---------------------super accelarated ln2----------------------------------------")
  (println "----------------------------------------------------------------------------------")
  (display-stream saln2 5)
  (println "----------------------------------------------------------------------------------")
  (println "I printed 100 terms for original ln2 stream, it did not close to ln2(0.69314718). For the accelerate-stream after printed 30 terms, it seemed faster close to ln2(0.69314718) than the original ln2 stream. Finally, when we use the super-accerlerate ln2 was just taking 5 terms to get to the exactly answer ln2(0.693147).")
  )
(run7)
