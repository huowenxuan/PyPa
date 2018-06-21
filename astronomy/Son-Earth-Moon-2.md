参考[运用Python 模拟太阳-地球-月亮运动模型](https://blog.csdn.net/huang_shiyang/article/details/78946448)
# 模型构建
现在假设历太阳-地球-月亮这个系统，太阳是旋转中心，地球相对太阳做角速度为ω1的匀速圆周运动，月球相对地球做ω2的匀速圆周运动。

以太阳为原点构建三维坐标系， 即太阳坐标点(x0,y0,z0) = (0,0,0) 
现假设地球公转的轨道平面（黄道面）在x-y轴平面上。

已知月球的轨道平面（白道面）与黄道面（地球的公转轨道平面）保持著5.145 396°的夹角，即与x-y轴平面呈5.145 396°的夹角

由于与x-y轴平面的夹角可以是任意方向的，为建模方便设月球公转轨道面沿y轴方向向上倾斜5.145 396°且初始状态时：太阳、地球、月球在y-z平面上（后文用φ表示月球公转轨道平面与地球公转轨道平面的固定夹角） 
假设地球公转半径为r1, 月球公转半径为r2， 
对于地球，假设其在t时刻时的坐标为(x1,y1,z1)，则有

<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
  <mrow>
    <mo>{</mo>
    <mtable columnalign="left right" rowspacing="4pt" columnspacing="1em">
      <mtr>
        <mtd>
          <msub>
            <mi>x</mi>
            <mn>1</mn>
          </msub>
          <mo>=</mo>
          <msub>
            <mi>x</mi>
            <mn>0</mn>
          </msub>
          <mo>+</mo>
          <msub>
            <mi>r</mi>
            <mn>1</mn>
          </msub>
          <mo>&#x22C5;<!-- ⋅ --></mo>
          <mi>cos</mi>
          <mo>&#x2061;<!-- ⁡ --></mo>
          <mrow>
            <mo>(</mo>
            <mrow>
              <msub>
                <mi>&#x03C9;<!-- ω --></mi>
                <mn>1</mn>
              </msub>
              <mi>t</mi>
            </mrow>
            <mo>)</mo>
          </mrow>
        </mtd>
      </mtr>
      <mtr>
        <mtd>
          <msub>
            <mi>y</mi>
            <mn>1</mn>
          </msub>
          <mo>=</mo>
          <msub>
            <mi>y</mi>
            <mn>0</mn>
          </msub>
          <mo>+</mo>
          <msub>
            <mi>r</mi>
            <mn>1</mn>
          </msub>
          <mo>&#x22C5;<!-- ⋅ --></mo>
          <mi>sin</mi>
          <mo>&#x2061;<!-- ⁡ --></mo>
          <mrow>
            <mo>(</mo>
            <mrow>
              <msub>
                <mi>&#x03C9;<!-- ω --></mi>
                <mn>1</mn>
              </msub>
              <mi>t</mi>
            </mrow>
            <mo>)</mo>
          </mrow>
        </mtd>
      </mtr>
      <mtr>
        <mtd>
          <msub>
            <mi>z</mi>
            <mn>1</mn>
          </msub>
          <mo>=</mo>
          <msub>
            <mi>z</mi>
            <mn>0</mn>
          </msub>
          <mo>+</mo>
          <mn>0</mn>
        </mtd>
        <mtd />
      </mtr>
    </mtable>
    <mo fence="true" stretchy="true" symmetric="true"></mo>
  </mrow>
</math>

现在对月球进行的运动轨迹进行建模: 任意t时刻，月球运行轨迹满足如下方程 

<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
  <mrow>
    <mo>{</mo>
    <mtable columnalign="left right" rowspacing="4pt" columnspacing="1em">
      <mtr>
        <mtd>
          <msub>
            <mi>z</mi>
            <mn>2</mn>
          </msub>
          <mo>=</mo>
          <msub>
            <mi>z</mi>
            <mn>1</mn>
          </msub>
          <mo>+</mo>
          <mrow>
            <mo>(</mo>
            <mrow>
              <msub>
                <mi>y</mi>
                <mn>2</mn>
              </msub>
              <mo>&#x2212;<!-- − --></mo>
              <msub>
                <mi>y</mi>
                <mn>1</mn>
              </msub>
            </mrow>
            <mo>)</mo>
          </mrow>
          <mo>&#x22C5;<!-- ⋅ --></mo>
          <mi>tan</mi>
          <mo>&#x2061;<!-- ⁡ --></mo>
          <mi>&#x03C6;<!-- φ --></mi>
        </mtd>
      </mtr>
      <mtr>
        <mtd>
          <msup>
            <mrow>
              <mo>(</mo>
              <mrow>
                <msub>
                  <mi>x</mi>
                  <mn>2</mn>
                </msub>
                <mo>&#x2212;<!-- − --></mo>
                <msub>
                  <mi>x</mi>
                  <mn>1</mn>
                </msub>
              </mrow>
              <mo>)</mo>
            </mrow>
            <mn>2</mn>
          </msup>
          <mo>+</mo>
          <msup>
            <mrow>
              <mo>(</mo>
              <mrow>
                <msub>
                  <mi>y</mi>
                  <mn>2</mn>
                </msub>
                <mo>&#x2212;<!-- − --></mo>
                <msub>
                  <mi>y</mi>
                  <mn>1</mn>
                </msub>
              </mrow>
              <mo>)</mo>
            </mrow>
            <mn>2</mn>
          </msup>
          <mo>+</mo>
          <msup>
            <mrow>
              <mo>(</mo>
              <mrow>
                <msub>
                  <mi>z</mi>
                  <mn>2</mn>
                </msub>
                <mo>&#x2212;<!-- − --></mo>
                <msub>
                  <mi>z</mi>
                  <mn>1</mn>
                </msub>
              </mrow>
              <mo>)</mo>
            </mrow>
            <mn>2</mn>
          </msup>
          <mo>=</mo>
          <msubsup>
            <mi>r</mi>
            <mn>2</mn>
            <mn>2</mn>
          </msubsup>
        </mtd>
        <mtd />
      </mtr>
    </mtable>
    <mo fence="true" stretchy="true" symmetric="true"></mo>
  </mrow>
</math>

月球初始方向向量为(0,cosφ,sinφ) 
在t时刻，月球转动的夹角ω2t, 此时的方向向量为(x2−x1,y2−y1,z2−z1) 
由向量夹角公式有， 

<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
  <msub>
    <mi>&#x03C9;<!-- ω --></mi>
    <mn>2</mn>
  </msub>
  <mi>t</mi>
  <mo>=</mo>
  <mrow>
    <mo>(</mo>
    <mrow>
      <msub>
        <mi>y</mi>
        <mn>2</mn>
      </msub>
      <mo>&#x2212;<!-- − --></mo>
      <msub>
        <mi>y</mi>
        <mn>1</mn>
      </msub>
    </mrow>
    <mo>)</mo>
  </mrow>
  <mo>&#x22C5;<!-- ⋅ --></mo>
  <mi>cos</mi>
  <mo>&#x2061;<!-- ⁡ --></mo>
  <mi>&#x03C6;<!-- φ --></mi>
  <mo>+</mo>
  <mrow>
    <mo>(</mo>
    <mrow>
      <msub>
        <mi>z</mi>
        <mn>2</mn>
      </msub>
      <mo>&#x2212;<!-- − --></mo>
      <msub>
        <mi>z</mi>
        <mn>1</mn>
      </msub>
    </mrow>
    <mo>)</mo>
  </mrow>
  <mo>&#x22C5;<!-- ⋅ --></mo>
  <mi>sin</mi>
  <mo>&#x2061;<!-- ⁡ --></mo>
  <mi>&#x03C6;<!-- φ --></mi>
</math>

联立上式，可得 

<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
  <mrow>
    <mo>{</mo>
    <mtable columnalign="left right" rowspacing="4pt" columnspacing="1em">
      <mtr>
        <mtd>
          <msub>
            <mi>x</mi>
            <mn>2</mn>
          </msub>
          <mo>=</mo>
          <msub>
            <mi>x</mi>
            <mn>1</mn>
          </msub>
          <mo>+</mo>
          <msub>
            <mi>r</mi>
            <mn>2</mn>
          </msub>
          <mo>&#x22C5;<!-- ⋅ --></mo>
          <mi>sin</mi>
          <mo>&#x2061;<!-- ⁡ --></mo>
          <mrow>
            <mo>(</mo>
            <mrow>
              <msub>
                <mi>&#x03C9;<!-- ω --></mi>
                <mn>2</mn>
              </msub>
              <mi>t</mi>
            </mrow>
            <mo>)</mo>
          </mrow>
        </mtd>
      </mtr>
      <mtr>
        <mtd>
          <msub>
            <mi>y</mi>
            <mn>2</mn>
          </msub>
          <mo>=</mo>
          <msub>
            <mi>y</mi>
            <mn>1</mn>
          </msub>
          <mo>+</mo>
          <mfrac>
            <mrow>
              <msub>
                <mi>r</mi>
                <mn>2</mn>
              </msub>
              <mo>&#x22C5;<!-- ⋅ --></mo>
              <mi>cos</mi>
              <mo>&#x2061;<!-- ⁡ --></mo>
              <mrow>
                <mo>(</mo>
                <mrow>
                  <msub>
                    <mi>&#x03C9;<!-- ω --></mi>
                    <mn>2</mn>
                  </msub>
                  <mi>t</mi>
                </mrow>
                <mo>)</mo>
              </mrow>
            </mrow>
            <mrow>
              <mi>cos</mi>
              <mo>&#x2061;<!-- ⁡ --></mo>
              <mi>&#x03C6;<!-- φ --></mi>
              <mrow>
                <mo>(</mo>
                <mrow>
                  <mn>1</mn>
                  <mo>+</mo>
                  <msup>
                    <mi>tan</mi>
                    <mn>2</mn>
                  </msup>
                  <mo>&#x2061;<!-- ⁡ --></mo>
                  <mi>&#x03C6;<!-- φ --></mi>
                </mrow>
                <mo>)</mo>
              </mrow>
            </mrow>
          </mfrac>
        </mtd>
      </mtr>
      <mtr>
        <mtd>
          <msub>
            <mi>z</mi>
            <mn>2</mn>
          </msub>
          <mo>=</mo>
          <msub>
            <mi>z</mi>
            <mn>1</mn>
          </msub>
          <mo>+</mo>
          <mrow>
            <mo>(</mo>
            <mrow>
              <msub>
                <mi>y</mi>
                <mn>2</mn>
              </msub>
              <mo>&#x2212;<!-- − --></mo>
              <msub>
                <mi>y</mi>
                <mn>1</mn>
              </msub>
            </mrow>
            <mo>)</mo>
          </mrow>
          <mo>&#x22C5;<!-- ⋅ --></mo>
          <mi>tan</mi>
          <mo>&#x2061;<!-- ⁡ --></mo>
          <mi>&#x03C6;<!-- φ --></mi>
        </mtd>
        <mtd />
      </mtr>
    </mtable>
    <mo fence="true" stretchy="true" symmetric="true"></mo>
  </mrow>
</math>

# 常数

日地距离：约1.5亿千米,即一个天文单位. 

月地距离：约38.4万千米 

因此 r1/r2=390.625
