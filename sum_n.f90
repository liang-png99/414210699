program sum_n
  implicit none
  integer(8) :: n, i, total
  character(len=32) :: arg
  integer :: ios

  if (command_argument_count() >= 1) then
    call get_command_argument(1, arg)
    read(arg, *, iostat=ios) n
  else
    write(*, '(A)', advance='no') 'Enter N: '
    read(*, *, iostat=ios) n
  end if

  if (ios /= 0 .or. n < 1) then
    write(*, '(A)') 'Error: N must be a positive integer.'
    stop 1
  end if

  total = 0
  do i = 1, n
    total = total + i
  end do

  write(*, '(A,I0,A,I0)') 'Sum of 1 to ', n, ' = ', total
end program sum_n
