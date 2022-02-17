
if !has('nvim-0.6.0')
  echoerr "requires at least nvim-0.6.0"
  finish
end

if exists('g:loaded_highlight_qf')
  finish
endif

let g:loaded_highlight_qf = 1


command -nargs=1 -complete=customlist,ListHighlightQFCommands HighlightQF lua require("highlight-qf").run(<f-args>)

fun ListHighlightQFCommands(A,L,P)
    return ['refresh', 'enable', 'disable', 'toggle'] 
endfun

autocmd QuickFixCmdPost * HighlightQF refresh
autocmd BufEnter        * HighlightQF refresh

