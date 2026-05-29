import { useState, useRef, useCallback } from 'react';
import './CodeEditor.css';

const LANGUAGES = [
  { value: 'python', label: 'Python' },
  { value: 'javascript', label: 'JavaScript' },
  { value: 'java', label: 'Java' },
  { value: 'cpp', label: 'C++' },
  { value: 'c', label: 'C' },
];

export default function CodeEditor({
  code = '',
  onChange,
  language = 'python',
  onLanguageChange,
  readOnly = false,
  minRows = 20,
}) {
  const textareaRef = useRef(null);
  const [localCode, setLocalCode] = useState(code);

  const currentCode = onChange ? code : localCode;

  const lines = currentCode.split('\n');
  const lineCount = Math.max(lines.length, minRows);

  const handleChange = useCallback((e) => {
    const value = e.target.value;
    if (onChange) {
      onChange(value);
    } else {
      setLocalCode(value);
    }
  }, [onChange]);

  const handleKeyDown = useCallback((e) => {
    if (e.key === 'Tab') {
      e.preventDefault();
      const textarea = textareaRef.current;
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const newValue = currentCode.substring(0, start) + '    ' + currentCode.substring(end);
      if (onChange) {
        onChange(newValue);
      } else {
        setLocalCode(newValue);
      }
      // Restore cursor position
      requestAnimationFrame(() => {
        textarea.selectionStart = textarea.selectionEnd = start + 4;
      });
    }
  }, [currentCode, onChange]);

  const handleScroll = useCallback((e) => {
    const lineNumbers = e.target.parentElement.querySelector('.editor-line-numbers');
    if (lineNumbers) {
      lineNumbers.scrollTop = e.target.scrollTop;
    }
  }, []);

  return (
    <div className="code-editor-wrapper">
      {/* Toolbar */}
      <div className="editor-toolbar">
        <div className="editor-toolbar-left">
          <div className="editor-dots">
            <span className="dot dot-red"></span>
            <span className="dot dot-yellow"></span>
            <span className="dot dot-green"></span>
          </div>
          <span className="editor-filename">solution.{language === 'python' ? 'py' : language === 'javascript' ? 'js' : language === 'java' ? 'java' : language === 'cpp' ? 'cpp' : 'c'}</span>
        </div>
        <div className="editor-toolbar-right">
          <select
            className="editor-language-select"
            value={language}
            onChange={(e) => onLanguageChange && onLanguageChange(e.target.value)}
          >
            {LANGUAGES.map((lang) => (
              <option key={lang.value} value={lang.value}>{lang.label}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Editor body */}
      <div className="editor-body">
        <div className="editor-line-numbers" aria-hidden="true">
          {Array.from({ length: lineCount }, (_, i) => (
            <div key={i} className="line-number">{i + 1}</div>
          ))}
        </div>
        <textarea
          ref={textareaRef}
          className="editor-textarea"
          value={currentCode}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          onScroll={handleScroll}
          spellCheck={false}
          autoComplete="off"
          autoCorrect="off"
          autoCapitalize="off"
          readOnly={readOnly}
          rows={minRows}
          placeholder={`// Start coding in ${LANGUAGES.find(l => l.value === language)?.label || language}...`}
        />
      </div>
    </div>
  );
}
