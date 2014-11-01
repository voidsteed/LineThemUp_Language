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
  (println (ecf 3) " ecf(3) ")
  (println (ecf 4) " ecf(4) ")
  (println (ecf 5) " ecf(5) ")
  (println (ecf 6) " ecf(6) ")
  )

(run8)
