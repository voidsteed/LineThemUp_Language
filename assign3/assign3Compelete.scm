;AUTHOR: Kaleb Williams kcwilliams3@crimson.ua.edu
;AUTHOR: Yujun Liu yliu59@crimson.ua.edu
;AUTHOR: Ben Halbach bhalbach@crimson.ua.edu

;**********************************Problem 1**********************************;
(define (replace func sym val)
  (cond
   ((eq? val +) (assign val '+))
   ((eq? val -) (assign val '-))
   ((eq? val *) (assign val '*))
   ((eq? val /) (assign val '/))
   ((eq? val %) (assign val '%))
   )
  (define (checkAndReplace oldVal)
    (cond
     ((list? oldVal) (map checkAndReplace oldVal))
     ((eq? oldVal sym) val)
     (else oldVal)
     )
    )
  (assign (dot func code) (cons 'begin (list (map checkAndReplace (cadr (dot func code))))))
  )
;*****************************************************************************;
;**********************************Problem 2**********************************;
(define (node rank item next)
  this
  )

(define (PRQ comparator)
  (define head (node nil nil nil))
  (define queue_size 0)
  (define (insert rank item) 
    (define spot head)
    (while (and (valid? (dot spot next))(comparator (dot spot next rank) rank))
	   (assign spot (dot spot next))
	   )
    (assign (dot spot next) (node rank item (dot spot next)))
    (++ queue_size)
    item
    )
  (define (item)
    (cond
     ((eq? (dot head next) nil) nil)
     (else (dot (dot head next) item))
     )
    )
  (define (remove)
    (define result (item))
    (assign (dot head next) (dot head next next))
    (-- queue_size)
    result
    )
  (define (rank)
    (cond
     ((eq? (dot head next) nil) nil)
     (else (dot (dot head next) rank))
     )
    )
  (define (empty?)
    (== queue_size 0)
    )
  (define (size)
    queue_size
    )
  (lambda (@) (apply (get (car @) __context) (cdr @)))
  )

(define p nil)
;*****************************************************************************;
;**********************************Problem 3**********************************;
(define (sim)
  (define time 0)
  (define events (PRQ <=))
  (define (add event delay)
    (events 'insert (+ time delay) event)
    )
  (define (run)
    (while (not (events 'empty?))
	   (set! time (events 'rank))
	   ((events 'remove))
	   )
    )
  this
  )

(define (wire)
  (define value 0)
  (define dstream nil)
  (define (register action)
    (set! dstream (cons action dstream))
    (action)
    )
  (define (get-value) value)
  (define (set-value v)
    (cond
     ((not (= value v))
      (set! value v)
      (define a)
      (for-each2 a dstream
		 (a)
		 )
      )
     )
    v
    )
  this
  )

(define (make-wire) (wire))

(define (get-signal wire) ((dot wire get-value)))

(define (set-signal! wire new-value) ((dot wire set-value) new-value))

(define (add-action! wire action-procedure) ((dot wire register) action-procedure))

(define (make-agenda) (sim))
(define x3 (make-wire))
(define x2 (make-wire))
(define x1 (make-wire))
(define x0 (make-wire))
(define y3 (make-wire))
(define y2 (make-wire))
(define y1 (make-wire))
(define y0 (make-wire))
(define o3 (make-wire))
(define o2 (make-wire))
(define o1 (make-wire))
(define o0 (make-wire))
(define cout (make-wire))


(define (propagate)
  ((dot the-agenda run))
  )

(define the-agenda (make-agenda))

(define (and-gate in1 in2 out)
  (define delay 5)
  (define (action)
    (define v1 (get-signal in1))
    (define v2 (get-signal in2))
    (define result (logical-and v1 v2))
    ((dot the-agenda add)
     (lambda ()
       (set-signal! out result)
       )
     delay
     )
    )
  (add-action! in1 action)
  (add-action! in2 action)
  )

(define (logical-and s1 s2)
  (if (and (= s1 1) (= s2 1))
      1
      0
      )
  )

(define (or-gate in1 in2 out)
  (define delay 5)
  (define (action)
    (define v1 (get-signal in1))
    (define v2 (get-signal in2))
    (define result (logical-or v1 v2))
    ((dot the-agenda add)
     (lambda ()
       (set-signal! out result)
       )
     delay
     )
    )
  (add-action! in1 action)
  (add-action! in2 action)
  )

(define (logical-or s1 s2)
  (if (or (= s1 1) (= s2 1))
      1
      0
      )
  )

(define (inverter in out)
  (define delay 5)
  (define (action)
    (define v (get-signal in))
    (define result (logical-not v))
    ((dot the-agenda add)
     (lambda ()
       (set-signal! out result)
       )
     delay
     )
    )
  (add-action! in action)
  )

(define (logical-not s)
  (if (= s 0)
      1
      0)
  )

(define (half-adder a b s c)
  (define d (make-wire))
  (define e (make-wire))
  (or-gate a b d)
  (and-gate a b c)
  (inverter c e)
  (and-gate d e s)
  )

(define (add1 a b c-in sum c-out)
  (define s (make-wire))
  (define c1 (make-wire))
  (define c2 (make-wire))
  (half-adder b c-in s c1)
  (half-adder a s sum c2)
  (or-gate c1 c2 c-out)
  )

(define (add4 x y o cout)
  (define x3 (car x))
  (define x2 (cadr x))
  (define x1 (caddr x))
  (define x0 (cadddr x))
  (define y3 (car y))
  (define y2 (cadr y))
  (define y1 (caddr y))
  (define y0 (cadddr y))
  (define o3 (car o))
  (define o2 (cadr o))
  (define o1 (caddr o))
  (define o0 (cadddr o))
  (define cin (make-wire))
  (define c0 (make-wire))
  (define c1 (make-wire))
  (define c2 (make-wire))
  (add1 x0 y0 cin o0 c0)
  (add1 x1 y1 c0 o1 c1)
  (add1 x2 y2 c1 o2 c2)
  (add1 x3 y3 c2 o3 cout)
  )

(define (clear-wires)
  (set-signal! x3 0)
  (set-signal! x2 0)
  (set-signal! x1 0)
  (set-signal! x0 0)
  (set-signal! y3 0)
  (set-signal! y2 0)
  (set-signal! y1 0)
  (set-signal! y0 0)
  (set-signal! o3 0)
  (set-signal! o2 0)
  (set-signal! o1 0)
  (set-signal! o0 0)
  (set-signal! cout 0)
  )

;*****************************************************************************;
;**********************************Problem 4**********************************;
(define (gravity f m1 m2 r)
  (define x (make-connector))
  (define y (make-connector))
  (define z (make-connector))
  (define G (make-connector))
  (multiplier m1 m2 y)
  (squarer r z)
  (multiplier G y x)
  (divider x z f)
  (constant 0.00667300 G)
  )

(define (multiplier m1 m2 product)
  (define (process-new-value)
    (cond ((or (and (has-value? m1) (= (get-value m1) 0))
	       (and (has-value? m2) (= (get-value m2) 0)))
	   (set-value! product 0 me)
	   )
	  ((and (has-value? m1) (has-value? m2))
	   (set-value! product
		       (* (get-value m1) (get-value m2))
		       me
		       )
	   )
	  ((and (has-value? product) (has-value? m1))
	   (set-value! m2
		       (/ (real(get-value product)) (get-value m1))
		       me
		       )
	   )
	  ((and (has-value? product) (has-value? m2))
	   (set-value! m1
		       (/ (real(get-value product)) (get-value m2))
		       me
		       )
	   )
	  )
    )
  (define (process-forget-value)
    (forget-value! product me)
    (forget-value! m1 me)
    (forget-value! m2 me)
    (process-new-value)
    )
  (define (me request)
    (cond
     ((eq? request 'I-have-a-value)
      (process-new-value))
     ((eq? request 'I-lost-my-value)
      (process-forget-value))
     )
    )
  (connect m1 me)
  (connect m2 me)
  (connect product me)
  me
  )

(define (divider dividend divisor quo)
  (define (process-new-value)
    (cond ((and (has-value? divisor) (=(get-value divisor)) 1)
	   (set-value! quo dividend me)
	   )
	  ((and (has-value? dividend) (has-value? divisor))
	   (set-value! quo
		       (/ (real (get-value dividend)) (get-value divisor))
		       me
		       )
	   )
	  ((and (has-value? quo) (has-value? dividend))
	   (set-value! divisor
		       (/ (real (get-value dividend)) (get-value quo))
		       me
		       )
	   )
	  ((and (has-value? quo) (has-value? divisor))
	   (set-value! dividend
		       (* (get-value quo) (get-value divisor))
		       me
		       )
	   )
	  )
    )
  (define (process-forget-value)
    (forget-value! quo me)
    (forget-value! dividend me)
    (forget-value! divisor me)
    (process-new-value)
    )
  (define (me request)
    (cond
     ((eq? request 'I-have-a-value)
      (process-new-value))
     ((eq? request 'I-lost-my-value)
      (process-forget-value))
     )
    )
  (connect dividend me)
  (connect divisor me)
  (connect quo me)
  me
  )

(define (squarer to-be-squared to-be-rooted)
  (define (process-new-value)
    (cond 
     ((has-value? to-be-squared)
      (set-value! to-be-rooted
		  (let ((in (get-value to-be-squared)))
		    (* in in)
		    )
		  me
		  )
      )
     ((has-value? to-be-rooted)
      (set-value! to-be-squared
		  (sqrt (get-value to-be-rooted))
		  me
		  )
      )
     )
    )
  (define (process-forget-value)
    (forget-value! to-be-squared me)
    (forget-value! to-be-rooted me)
    (process-new-value)
    )
  (define (me request)
    (cond 
     ((eq? request 'I-have-a-value)
      (process-new-value))
     ((eq? request 'I-lost-my-value)
      (process-forget-value))
     )
    )
  (connect to-be-squared me)
  (connect to-be-rooted me)
  me
  )

(define (constant value connector)
  (define (me request))
  (connect connector me)
  (set-value! connector value me)
  me
  )

(define (find items x)
  (cond
   ((null? items) #f)
   ((eq? x (car items)) #t)
   (else (find (cdr items) x))
   )
  )

(define (make-connector)
  (define value #f)
  (define informant #f)
  (define constraints '())
  (define (set-my-value newval setter)
    (cond 
     ((not (has-value? me))
      (set! value newval)
      (set! informant setter)
      (for-each-except setter
		       inform-about-value
		       constraints
		       )
      )
     )
    )
  (define (forget-my-value retractor)
    (if informant
	(begin
	;                (set! value #f)
	  (if (eq? retractor informant)
	      (begin (set! informant #f)
		     (for-each-except retractor
				      inform-about-no-value
				      constraints
				      )
		     )
	      )
	  )
	)
    )
  (define (connect new-constraint)
    (if (not (find  constraints new-constraint))
	(set! constraints
	      (cons new-constraint constraints)
	      )
	)
    (if (has-value? me)
	(inform-about-value new-constraint)
	)
    )
  (define (me request)
    (cond
     ((eq? request 'has-value?) (if informant #t #f))
     ((eq? request 'value) value)
     ((eq? request 'set-value!) set-my-value)
     ((eq? request 'forget) forget-my-value)
     ((eq? request 'connect) connect)
     )
    )
  me
  )

(define (for-each-except exception procedure list)
  (define (loop items)
    (cond ((null? items) 'done)
	  ((eq? (car items) exception) (loop (cdr items)))
	  (else (procedure (car items))
                (loop (cdr items))
                )
	  )
    )
  (loop list)
  )

(define (has-value? connector)
  (connector 'has-value?)
  )

(define (get-value connector)
  (connector 'value)
  )

(define (set-value! connector new-value informant)
  ((connector 'set-value!) new-value informant)
  )

(define (forget-value! connector retractor)
  ((connector 'forget) retractor)
  )

(define (connect connector new-constraint)
  ((connector 'connect) new-constraint)
  )

(define (inform-about-value constraint)
  (constraint 'I-have-a-value)
  )

(define (inform-about-no-value constraint)
  (constraint 'I-lost-my-value)
  )

(define f (make-connector))
(define m1 (make-connector))
(define m2 (make-connector))
(define r (make-connector))

;*****************************************************************************;


;**********************************Problem 5**********************************;

; Some stream functions
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
; End stream functions

; Some streams
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
; End streams

(define (alt s)
  (define alt-ones
    (cons-stream
     1
     (cons-stream -1 alt-ones)))
  (stream-map * s alt-ones)
  )

(define (addsub s)
  (define (helper s)
    (cons-stream
     (stream-car s)
     (stream-add
      (stream-cdr s)
      (helper s)
      )
     )
    )
  (helper (alt s))
  )


;*****************************************************************************;


;**********************************Problem 6**********************************;

; Some basic stream functions

(define scons cons-stream)
(define scar stream-car)
(define scdr stream-cdr)

(define (sref s n)
  (if (= n 0)
      (scar s)
      (sref (scdr s) (- n 1)))
  )

(define (sadd s t)
  (scons
   (+ (scar s) (scar t))
   (sadd
    (scdr s)
    (scdr t))
   )
  )

(define (smap f s)
  (scons (f (scar s))
	 (smap f (scdr s)))
  )

(define (sdisplay s n)
  (cond ((= n 0) (println "..."))
	(else 
	 (print (scar s) " ")
	 (sdisplay (scdr s) (- n 1))
	 )
	)
  )

(define (combine s t p?)
  (if (p? (scar s) (scar t))
      (scons (scar s)
	     (combine (scdr s) t p?))
      (scons (scar t)
	     (combine (scdr t) s p?)))
  )

(define (weave s t)
  (scons (scar s)
	 (weave t (scdr s)))
  )

(define Ones (scons 1 Ones))
(define naturals (scons 1 (sadd Ones naturals)))

(define (sremove p? s)
  (if (p? (stream-car s))
      (sremove p? (scdr s))
      (scons
       (scar s)
       (sremove p? (scdr s))))
  )

(define (sieve nums)
  (scons (scar nums)
	 (sieve (sremove 
		 (lambda (x) (= (% x (scar nums)) 0))
		 (scdr nums))))
  )

(define primes (sieve (scdr naturals)))

(define (remove-repeats s)
  (define s1 (sref s 1))
  (define s0 (sref s 0))
  (if (equal? s0 s1)
      (remove-repeats (scdr s))
      (scons s0 (remove-repeats (scdr s))))
  )

; End basic stream functions

(define (twinFilter s)
  (define s1 (sref s 1))
  (define s0 (sref s 0))
  (if (= (- s1 s0) 2)
      (scons (list s0 s1)
	     (twinFilter (scdr s)))
      (twinFilter (scdr s)))
  )

(define (twinPrimes)
  (twinFilter primes)
  )

;*****************************************************************************;


;**********************************Problem 7**********************************;

(define (stream-ref s n)
  (cond
   ((= n 0) 
    (stream-car s))
   (else
    (stream-ref (stream-cdr s) (- n 1))
    )))

(define (square2 x)
  (* x x))

(define (euler-transform s)
  (let ((s0 (stream-ref s 0))
        (s1 (stream-ref s 1))
        (s2 (stream-ref s 2)))
    (cond  
     ((= (+ s0 s2) (* 2 s1))
      (println "caught a divide 0")
      s)
     (else
      (cons-stream (- s2 (/ (square2 (- s2 s1))
			    (+ s0 (* -2 s1) s2)))
		   (euler-transform (stream-cdr s))))
     ))
  )

(define (log-summands n)
  (cons-stream (/ 1.0 n)
               (stream-map - (log-summands (+ n 1)))))

(define ln2
  (psum (log-summands 1)))

(define aln2 (euler-transform ln2))

(define (make-tableau transform s)
  (cons-stream s
               (make-tableau transform
                     (transform s))))

(define (acc-seq transform s)
  (stream-map stream-car
              (make-tableau transform s)))

(define saln2 (acc-seq euler-transform ln2))

(define (stream-check s tolerance)
  (define s0 (stream-car s))
  (define s1 (stream-car (stream-cdr s)))
  (if (< (- tolerance) (- s0 s1) tolerance)
      1
      (+ 1 (stream-check (stream-cdr s) tolerance)))
  )
  
;*****************************************************************************;


;**********************************Problem 8**********************************;

(define (pairs is js)
  (scons (list (scar is) (scar js))
	 (weave (smap (lambda (x) (list (scar is) x)) (scdr js))
		(pairs (scdr is) js)))
  )

(define (neg s)
  (smap (lambda (x) (- x)) s)
  )

(define Ints 
  (scons 0 (weave naturals (neg naturals)))
  )

(define all-pairs 
  (pairs Ints Ints)
  )

;*****************************************************************************;


;**********************************Problem 9**********************************;

(define (cube x)
  (* x x x)
  )

(define (sumCube2 a)
  (+ (cube (car a)) (cube (cadr a)))
  )

(define (sumCubeComp2 a b)
  (< (sumCube2 a) (sumCube2 b))
  )

(define (rama-pairs is js)
  (scons 
   (list (scar is) (scar js))
   (combine
    (smap (lambda (x) (list (scar is) x)) (scdr js))
    (rama-pairs (scdr is) (scdr js))
    sumCubeComp2))
  )

(define (rama)
  (define (helper p)
    (define s1 (sref p 1))
    (define s0 (sref p 0))
    (if (= (sumCube2 s0) (sumCube2 s1))
	(scons (sumCube2 s0)
	       (helper (scdr (scdr p))))
	(helper (scdr p)))
    )
  (helper (rama-pairs naturals naturals))
  )

;*****************************************************************************;



;**********************************Run Funcs**********************************;

(define (run1)
  (define (square x) (* x x))
  (define (addThreeSquares x y z) (+ (* x x) (* y y) (* z z)))
  (println "***********************************Problem 1***********************************")
  (inspect (dot square code))
  (inspect (square 5))
  (println)
  (println "Performing (replace square '* +).")
  (replace square '* +)
  (inspect (dot square code))
  (inspect (square 5))
  (println)
  (println "Performing (replace square 'x 2).")
  (replace square 'x 2)
  (inspect (dot square code))
  (inspect (square 5))
  (println "\n")
  (inspect (dot addThreeSquares code))
  (inspect (addThreeSquares 1 2 3))
  (println)
  (println "Performing (replace addThreeSquares '* +).")
  (replace addThreeSquares '* +)
  (inspect (dot addThreeSquares code))
  (inspect (addThreeSquares 1 2 3))
  (println "*******************************************************************************")
  )

(define (run2)
  (println "***********************************Problem 2***********************************")
  (define (checkPRQ p)
    (inspect (p 'item))
    (inspect (p 'rank))
    (inspect (p 'size))
    (inspect (p 'empty?))
    (println)
    )

  (println "Calling (set! p (PRQ >))")	
  (set! p (PRQ >))
  (checkPRQ p)
  (inspect (p 'insert 0 5))
  (checkPRQ p)
  (inspect (p 'insert 3 10))
  (checkPRQ p)
  (inspect (p 'insert 2 1))
  (checkPRQ p)
  (inspect (p 'insert -5 266))
  (checkPRQ p)
  (inspect (p 'remove))
  (checkPRQ p)
  (inspect (p 'insert 2 0))
  (checkPRQ p)
  (inspect (p 'remove))
  (checkPRQ p)
  (inspect (p 'remove))
  (checkPRQ p)
  (inspect (p 'remove))
  (checkPRQ p)
  (inspect (p 'remove))
  (checkPRQ p)
  (println)
  (println "Calling (set! p (PRQ <=))")	
  (set! p (PRQ <=))
  (checkPRQ p)
  (inspect (p 'insert 0 5))
  (checkPRQ p)
  (inspect (p 'insert 3 10))
  (checkPRQ p)
  (inspect (p 'insert 0 12))
  (checkPRQ p)
  (inspect (p 'remove))
  (checkPRQ p)
  (println "*******************************************************************************")
  )

(define (run3)
  (println "***********************************Problem 3***********************************")
  (inspect (get-signal x3))
  (inspect (get-signal x2))
  (inspect (get-signal x1))
  (inspect (get-signal x0))
  (inspect (get-signal y3))
  (inspect (get-signal y2))
  (inspect (get-signal y1))
  (inspect (get-signal y0))
  (println "Creating 4-bit ripple carry adder.")
  (add4 (list x3 x2 x1 x0) (list y3 y2 y1 y0) (list o3 o2 o1 o0) cout)
  (inspect (set-signal! x3 1))
  (inspect (set-signal! x2 0))
  (inspect (set-signal! x1 0))
  (inspect (set-signal! x0 1))
  (inspect (set-signal! y3 1))
  (inspect (set-signal! y2 0))
  (inspect (set-signal! y1 1))
  (inspect (set-signal! y0 1))
  (inspect (get-signal cout))
  (inspect (get-signal o3))
  (inspect (get-signal o2))
  (inspect (get-signal o1))
  (inspect (get-signal o0))
  (println "Propogating...")
  (propagate)
  (inspect (get-signal cout))
  (inspect (get-signal o3))
  (inspect (get-signal o2))
  (inspect (get-signal o1))
  (inspect (get-signal o0))
  (println "[should be 1 0 1 0 0]")
  (newline)
  (inspect (set-signal! x3 1))
  (inspect (set-signal! x2 1))
  (inspect (set-signal! x1 1))
  (inspect (set-signal! x0 0))
  (inspect (set-signal! y3 0))
  (inspect (set-signal! y2 0))
  (inspect (set-signal! y1 1))
  (inspect (set-signal! y0 1))
  (inspect (get-signal cout))
  (inspect (get-signal o3))
  (inspect (get-signal o2))
  (inspect (get-signal o1))
  (inspect (get-signal o0))
  (println "Propogating...")
  (propagate)
  (inspect (get-signal cout))
  (inspect (get-signal o3))
  (inspect (get-signal o2))
  (inspect (get-signal o1))
  (inspect (get-signal o0))
  (println "*******************************************************************************")
  )

(define (run4)
  (println "***********************************Problem 4***********************************")
  (inspect f)
  (inspect m1)
  (inspect m2)
  (inspect r)
  (gravity f m1 m2 r)
  (println "setting values: f=10, m1=50, m2=2")
  (set-value! f 10 'user)
  (set-value! m1 50 'user)
  (set-value! m2 2 'user)
  (inspect (get-value f))
  (inspect (get-value m1))
  (inspect (get-value m2))
  (inspect (get-value r))
  (println "[should be .2583215051]") 
  (forget-value! f 'user)
  (forget-value! m1 'user)
  (forget-value! m2 'user)
  (println)
  (println "setting values: m1=50, m2=2, r=.2583215051")
  (set-value! m1 50 'user)
  (set-value! m2 2 'user)
  (set-value! r .2583215051 'user)
  (inspect (get-value m1))
  (inspect (get-value m2))
  (inspect (get-value r))
  (inspect (get-value f))
  (println "[should be 10]")
  (forget-value! r 'user)
  (forget-value! m1 'user)
  (forget-value! m2 'user)
  (println "*******************************************************************************")
  )

(define (run5)
  (println "***********************************Problem 5***********************************")
  (define z (addsub (ints)))
  (print "The numeric stream result is: " )
  (sdisplay z 10)
  (println "It should be 0 -1 1 -2 2 -3 3 -4 4 -5 ...")
  (println "*******************************************************************************")
  )

(define (run6)
  (println "***********************************Problem 6***********************************")
  (println "The stream of twin primes (up to the first 5) goes like:")
  (sdisplay (twinPrimes) 5)
  (println)
  (println "*******************************************************************************")
  )

(define (run7)
  (println "***********************************Problem 7***********************************")
  (println "----------------------------------------------------------------------------------")
  (println "---------------------unaccelarate ln2---------------------------------------------")
  (println "----------------------------------------------------------------------------------")
  (display-stream ln2 5)
  (println "Converges to 0.1 in " (stream-check ln2 .1) " iterations.")
  ;(display-stream ln2 10)
  (println "----------------------------------------------------------------------------------")
  (println "---------------------accelarated ln2----------------------------------------------")
  (println "----------------------------------------------------------------------------------")
  (display-stream aln2 5)
  (println "Converges to 0.0001 in " (stream-check aln2 0.0001) " iterations.")
  ;(display-stream aln2 5)
  (println "----------------------------------------------------------------------------------")
  (println "---------------------super accelarated ln2----------------------------------------")
  (println "----------------------------------------------------------------------------------")
  (display-stream saln2 5)
  (println "Converges to 0.0001 in " (stream-check saln2 0.0001) " iterations.")
  ;(display-stream saln2 5)
  (println "----------------------------------------------------------------------------------")
  (println "*******************************************************************************")
  )

(define (run8)
  (println "***********************************Problem 8***********************************")
  (println "The stream of all pairs of integers (first 20) starts like:")
  (sdisplay all-pairs 20)
  (println "*******************************************************************************")
  )

(define (run9)
  (println "***********************************Problem 9***********************************")
  (println "The first 3 ramanujan numbers are: ")
  (sdisplay (rama) 3)
  (println "*******************************************************************************")
  )

;*****************************************************************************;
(display "\n\nassignment 3 loaded!\n\n")

