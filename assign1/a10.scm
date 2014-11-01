(define (ramanujan2 depth x)
  (define (recur count)
    (cond
      ((= count depth)
       1)
      (else
      (sqrt (+ 1 (* (recur (+ count 1)) (+ x count)))))
      )
    )
    (recur 0)
  )
(println "(ramanujan2 4 4)" (ramanujan2 4 4))
(println "[It should be 4.454771]")
(println "(ramanujan2 2 3)" (ramanujan2 2 3))
(println "[It should be 4.454771]")

